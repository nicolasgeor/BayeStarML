#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:50:13 2025

@author: LamirelFamily
"""

from preprocess import return_train_test, prepare_pred4, denormalise_val, prepare_pred3
from utils import get_dataset, train, mard, mrd
from models import hbnn, bart, gp
from pred_sampling import sample_post_pred_HBNN_para, posterior_predictive_GP
import arviz as az
import numpy as np
import pymc as pm
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_absolute_error

os.makedirs('Dataset_D_training_with_Xiong', exist_ok=True)

df_train = get_dataset('Datasets/database_D_old_format.txt', 'MS')
df_train = df_train[df_train['mode'] == 'A']
# (x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
#   mass_test, emass_test
# ) = return_train_test(df_train)
(x_train, x_train_er, x_test, x_test_err, rad_train, erad_train,
  rad_test, erad_test
) = return_train_test(df_train)

# unorm_mass = denormalise_val(mass_test, 'mass')
unorm_rad = denormalise_val(rad_test, 'radius')

x_train = x_train[['Teff', 'logg', 'Meta', 'L']]
x_train_er = x_train_er[['eTeff', 'elogg', 'eMeta', 'eL']]

x_test = x_test[['Teff', 'logg', 'Meta', 'L']]
x_test_er = x_test_err[['eTeff', 'elogg', 'eMeta', 'eL']]

# print(x_test3_er)

def main():

    print('A-label stars used after cleanup:', len(df_train))
    print('Training stars:', len(x_train))
    print('Test stars:', len(x_test))

    #######################################################################################
    # NOW, THIS IS BUILT FOR TRAINING ON RADIUS. FOR MASS, VARIABLE NAMES NEED TO BE CHANGED
    # MANUALLY; THERE'S NO WAY TO SWITCH BY JUST COMMENTING/UNCOMMENTING
    #######################################################################################

    # PICK ONE OF THESE TWO COMBINATIONS (model + trace)
    # If training HBNN: uncomment the next 2 lines, and comment the GP model + trace below.
 
    model = hbnn.HBNN_M4(x_train, rad_train, x_train_er, erad_train, 15)

    
    trace = train(model, "Dataset_D_training_with_Xiong/HBNN_rad_4param_L_3000_draws_4_chains_15_nodes_sig_015_seed_392.nc", draw=3000, chains=4)

    
    # If training GP: uncomment the next 2 lines, and comment the HBNN model + trace above.
    # model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(x_train,
    #                                                                     x_train_er,
    #                                                                     rad_train, 100, 50)
    
    # trace = train(model, "Dataset_D_training_with_Xiong/GP_rad_4param_L_3000_draws_4_chains_100_50_seed_392.nc", draw=3000, chains=4)
    
    r_hat_values = az.rhat(trace)
    all_rhats = []
    for var in r_hat_values.data_vars:
        max_rhat = r_hat_values[var].max().values.item()
        all_rhats.append((var, max_rhat))

    print(all_rhats)
    
    print(az.loo(trace))
    
    # PICK ONE OF THESE TWO PREDICTION BLOCKS.

    # pred, lpd = posterior_predictive_GP(
    #     model, μ_gp, log_var_gp, trace,
    #     x_test, x_test_er, Xu, Xu_er, 4, 'radius'
    # )

    pred, lpd = sample_post_pred_HBNN_para(
        trace, x_test, x_test_er, 15, 4, 'radius'
    )

    # pred, lpd = sample_post_pred_HBNN_para(trace, x_test, x_test_er, 15, 4, 'radius')

    R_pred_sigma = pred.std(0)
    R_pred_mean = pred.mean(0)

    print(R_pred_sigma)
    print(R_pred_mean)
    print(unorm_rad)
    
    print('MAE: ', mean_absolute_error(unorm_rad, R_pred_mean))
    
    print('MARD', mard(unorm_rad, R_pred_mean))
    
    print('MRD', mrd(unorm_rad, R_pred_mean))

    original_db = pd.read_table('Datasets/database_D_old_format.txt', sep='\t', comment='%')
    test_original_rows = original_db.loc[x_test.index]
    id_col = 'SIMBAD_ID' if 'SIMBAD_ID' in test_original_rows.columns else 'ID'
    residual_R = R_pred_mean - np.asarray(unorm_rad)
    diagnostic_table = pd.DataFrame({
        'original_row': x_test.index,
        'ID': test_original_rows[id_col].values if id_col in test_original_rows.columns else np.nan,
        'catalog': test_original_rows['catalog'].values if 'catalog' in test_original_rows.columns else np.nan,
        'R_true': np.asarray(unorm_rad),
        'R_pred': R_pred_mean,
        'R_pred_sigma': R_pred_sigma,
        'residual_R': residual_R,
        'abs_residual_R': np.abs(residual_R),
        'relative_error_pct': residual_R / np.asarray(unorm_rad) * 100,
        'abs_relative_error_pct': np.abs(residual_R / np.asarray(unorm_rad) * 100),
        'pull': np.where(R_pred_sigma != 0, residual_R / R_pred_sigma, np.nan),
        'abs_pull': np.abs(np.where(R_pred_sigma != 0, residual_R / R_pred_sigma, np.nan)),
    })
    # CHANGE THIS FILENAME
    diagnostic_table.to_csv('Dataset_D_training_with_Xiong/radius_prediction_results_HBNN_3000_seed_392.tsv', sep='\t', index=False)
    diagnostic_print_columns = ['original_row', 'ID', 'catalog', 'R_true', 'R_pred', 'R_pred_sigma',
                                'residual_R', 'abs_residual_R', 'relative_error_pct',
                                'abs_relative_error_pct', 'pull', 'abs_pull']

    print('\nTop 20 radius prediction errors by abs_relative_error_pct:')
    print(diagnostic_table.sort_values('abs_relative_error_pct', ascending=False).head(20).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 radius prediction uncertainties by R_pred_sigma:')
    print(diagnostic_table.sort_values('R_pred_sigma', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 radius prediction pulls by abs_pull:')
    print(diagnostic_table.sort_values('abs_pull', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    sigma_cut = np.percentile(R_pred_sigma, 95)
    plot_mask = R_pred_sigma < sigma_cut
    unorm_rad_plot = np.asarray(unorm_rad)[plot_mask]
    R_pred_mean_plot = R_pred_mean[plot_mask]
    R_pred_sigma_plot = R_pred_sigma[plot_mask]
    # Change this plot base to match the active GP or HBNN training filename above.
    # plot_output_base = 'Dataset_D_training_with_Xiong/GP_radius_4param_L_3000_draws_4_chains_100_50_seed_392'
    plot_output_base = 'Dataset_D_training_with_Xiong/HBNN_radius_4param_L_3000_draws_4_chains_15_nodes_sig_015_seed_392'

    # CHANGE NAMES HERE FOR THE PLOTS. 4 TIMES (ONE ABOVE AND THREE BELOW)

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_rad, R_pred_mean, yerr=R_pred_sigma, fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_rad.min(), unorm_rad.max()], [unorm_rad.min(), unorm_rad.max()], 'r--')
    plt.xlabel('True Radius')
    plt.ylabel('Predicted Radius')
    plt.title('HBNN Predictions with Uncertainty')
    plt.legend()
    plt.savefig(plot_output_base + '_full_prediction.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_rad, R_pred_mean - unorm_rad, yerr=R_pred_sigma, fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_rad.min(), unorm_rad.max(), 'r', linestyle='--')
    plt.xlabel('True Radius')
    plt.ylabel('Residual Radius')
    plt.title('HBNN Predictions with Uncertainty')
    plt.legend()
    plt.savefig(plot_output_base + '_full_residual.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_rad_plot, R_pred_mean_plot, yerr=R_pred_sigma_plot, fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_rad_plot.min(), unorm_rad_plot.max()], [unorm_rad_plot.min(), unorm_rad_plot.max()], 'r--')
    plt.xlabel('True Radius')
    plt.ylabel('Predicted Radius')
    plt.title('HBNN Predictions with Uncertainty (R_pred_sigma < 95th percentile)')
    plt.legend()
    plt.savefig(plot_output_base + '_filtered_prediction.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_rad_plot, R_pred_mean_plot - unorm_rad_plot, yerr=R_pred_sigma_plot, fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_rad_plot.min(), unorm_rad_plot.max(), 'r', linestyle='--')
    plt.xlabel('True Radius')
    plt.ylabel('Residual Radius')
    plt.title('HBNN Residual Radius (R_pred_sigma < 95th percentile)')
    plt.legend()
    plt.savefig(plot_output_base + '_filtered_residual.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()
