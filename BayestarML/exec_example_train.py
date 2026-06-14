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

OUTPUT_DIR = r'C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_A_training_13_june'
SAMPLING_SEED = 225

os.makedirs(OUTPUT_DIR, exist_ok=True)

df_train = get_dataset('Datasets/database_B.txt', 'MS', filter_mode='rho')
(x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
  mass_test, emass_test
) = return_train_test(df_train, feature_set='rho')

unorm_mass = denormalise_val(mass_test, 'mass')

x_train = x_train[['Teff', 'Meta', 'rho']]
x_train_er = x_train_er[['eTeff', 'eMeta', 'erho']]

x_test = x_test[['Teff', 'Meta', 'rho']]
x_test_er = x_test_err[['eTeff', 'eMeta', 'erho']]

# print(x_test3_er)

def main():


    # PiCK ONE OF THESE TWO COMBINATiONS (plot name + model + trace)
 
    # plot_model_name = 'HBNN'
    # model = hbnn.HBNN_M3(x_train, mass_train, x_train_er, emass_train, 15)

    
    # trace = train(model, os.path.join(OUTPUT_DIR, f"HBNN_mass_3param_L_1000_draws_4_chains_15_nodes_sig_015_seed_{SAMPLING_SEED}.nc"), draw=1000, chains=4, random_seed=SAMPLING_SEED)

    
    model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(x_train,
                                                                        x_train_er,
                                                                        mass_train, 80, 40)
    
    plot_model_name = 'GP'
    trace = train(model, os.path.join(OUTPUT_DIR, f"GP_mass_3param_L_1000_draws_4_chains_80_40_seed_{SAMPLING_SEED}.nc"), draw=1000, chains=4, random_seed=SAMPLING_SEED)

    
    # model = hbnn.HBNN_M4(x_train, rad_train, x_train_er, erad_train, 15)

    
    # Train is imported from another file, and runs MCMC sampling using PyMC.

    # trace = az.from_netcdf("Radius_output/HBNN_sig_015_15_nodes_mass_4_param.nc")
    
    # trace = train(model, "Radius_output/HBNN_sig_015_15_nodes_mass_4_param.nc", draw=1000, chains=2)

    # trace = az.from_netcdf("Radius_output/GP_hetero_new_2026_mass_4param_gamma_etav_80_40.nc")

    
        
    # trace.extend(pm.compute_log_likelihood(trace, model=model, var_names='y'))
    
    r_hat_values = az.rhat(trace)
    all_rhats = []
    for var in r_hat_values.data_vars:
        max_rhat = r_hat_values[var].max().values.item()
        all_rhats.append((var, max_rhat))

    print(all_rhats)
    
    print(az.loo(trace))
    
    # PICK ONE OF THESE TWO

    pred, lpd = posterior_predictive_GP(
        model, μ_gp, log_var_gp, trace,
        x_test, x_test_er, Xu, Xu_er, 3, 'mass'
    )

    # pred, lpd = sample_post_pred_HBNN_para(
    #     trace, x_test, x_test_er, 15, 3, 'mass'
    # )

    # pred, lpd = sample_post_pred_HBNN_para(trace, x_test, x_test_er, 15, 4, 'mass')

    M_pred_sigma = pred.std(0)
    M_pred_mean = pred.mean(0)

    print(M_pred_sigma)
    print(M_pred_mean)
    print(unorm_mass)
    
    print('MAE: ', mean_absolute_error(unorm_mass, M_pred_mean))
    
    print('MARD', mard(unorm_mass, M_pred_mean))
    
    print('MRD', mrd(unorm_mass, M_pred_mean))

    original_db = pd.read_table('Datasets/database_B.txt', sep='\t', comment='%')
    test_original_rows = original_db.loc[x_test.index]
    id_col = 'SIMBAD_ID' if 'SIMBAD_ID' in test_original_rows.columns else 'ID'
    residual_M = M_pred_mean - np.asarray(unorm_mass)
    diagnostic_table = pd.DataFrame({
        'original_row': x_test.index,
        'ID': test_original_rows[id_col].values if id_col in test_original_rows.columns else np.nan,
        'catalog': test_original_rows['catalog'].values if 'catalog' in test_original_rows.columns else np.nan,
        'M_true': np.asarray(unorm_mass),
        'M_pred': M_pred_mean,
        'M_pred_sigma': M_pred_sigma,
        'residual_M': residual_M,
        'abs_residual_M': np.abs(residual_M),
        'relative_error_pct': residual_M / np.asarray(unorm_mass) * 100,
        'abs_relative_error_pct': np.abs(residual_M / np.asarray(unorm_mass) * 100),
        'pull': np.where(M_pred_sigma != 0, residual_M / M_pred_sigma, np.nan),
        'abs_pull': np.abs(np.where(M_pred_sigma != 0, residual_M / M_pred_sigma, np.nan)),
    })
    diagnostic_table.to_csv(os.path.join(OUTPUT_DIR, f'mass_prediction_results_{plot_model_name}_1000_seed_{SAMPLING_SEED}.tsv'), sep='\t', index=False)
    diagnostic_print_columns = ['original_row', 'ID', 'catalog', 'M_true', 'M_pred', 'M_pred_sigma',
                                'residual_M', 'abs_residual_M', 'relative_error_pct',
                                'abs_relative_error_pct', 'pull', 'abs_pull']

    print('\nTop 20 mass prediction errors by abs_relative_error_pct:')
    print(diagnostic_table.sort_values('abs_relative_error_pct', ascending=False).head(20).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 mass prediction uncertainties by M_pred_sigma:')
    print(diagnostic_table.sort_values('M_pred_sigma', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 mass prediction pulls by abs_pull:')
    print(diagnostic_table.sort_values('abs_pull', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    sigma_cut = np.percentile(M_pred_sigma, 95)
    plot_mask = M_pred_sigma < sigma_cut
    unorm_mass_plot = np.asarray(unorm_mass)[plot_mask]
    M_pred_mean_plot = M_pred_mean[plot_mask]
    M_pred_sigma_plot = M_pred_sigma[plot_mask]
    plot_output_base = os.path.join(OUTPUT_DIR, f'GP_mass_3param_L_1000_draws_4_chains_80_40_seed_{SAMPLING_SEED}')
    # plot_output_base = os.path.join(OUTPUT_DIR, f'HBNN_mass_3param_L_1000_draws_4_chains_15_nodes_sig_015_seed_{SAMPLING_SEED}')

    # CHANGE NAMES HERE FOR THE PLOTS. ABOVE.

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass, M_pred_mean, yerr=M_pred_sigma, fmt='o',
                 color='black', markerfacecolor='black', markeredgecolor='black',
                 ecolor='cornflowerblue', label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_mass.min(), unorm_mass.max()], [unorm_mass.min(), unorm_mass.max()], 'r--')
    plt.xlabel('True Mass')
    plt.ylabel('Predicted Mass')
    plt.title(plot_model_name + ' Predictions with Uncertainty')
    plt.legend()
    plt.savefig(plot_output_base + '_full_prediction.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass, M_pred_mean - unorm_mass, yerr=M_pred_sigma, fmt='o',
                 color='black', markerfacecolor='black', markeredgecolor='black',
                 ecolor='cornflowerblue', label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_mass.min(), unorm_mass.max(), 'r', linestyle='--')
    plt.xlabel('True Mass')
    plt.ylabel('Residual Mass')
    plt.title(plot_model_name + ' Residual Mass')
    plt.legend()
    plt.savefig(plot_output_base + '_full_residual.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass_plot, M_pred_mean_plot, yerr=M_pred_sigma_plot, fmt='o',
                 color='black', markerfacecolor='black', markeredgecolor='black',
                 ecolor='cornflowerblue', label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_mass_plot.min(), unorm_mass_plot.max()], [unorm_mass_plot.min(), unorm_mass_plot.max()], 'r--')
    plt.xlabel('True Mass')
    plt.ylabel('Predicted Mass')
    plt.title(plot_model_name + ' Predictions with Uncertainty (M_pred_sigma < 95th percentile)')
    plt.legend()
    plt.savefig(plot_output_base + '_filtered_prediction.png', dpi=300, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass_plot, M_pred_mean_plot - unorm_mass_plot, yerr=M_pred_sigma_plot, fmt='o',
                 color='black', markerfacecolor='black', markeredgecolor='black',
                 ecolor='cornflowerblue', label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_mass_plot.min(), unorm_mass_plot.max(), 'r', linestyle='--')
    plt.xlabel('True Mass')
    plt.ylabel('Residual Mass')
    plt.title(plot_model_name + ' Residual Mass (M_pred_sigma < 95th percentile)')
    plt.legend()
    plt.savefig(plot_output_base + '_filtered_residual.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()
