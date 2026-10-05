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

#######################################################################################
# EXECUTION CONFIGURATION
#######################################################################################
# Set to "HBNN" or "GP"
ACTIVE_MODEL = "GP"  
TARGET_VAR = "radius"  # Set to "radius" or "mass"
SHOW_PLOTS = True     # True to pop up plots (plt.show), False for background runs (plt.close)

SEED = 239
DRAWS = 3000
CHAINS = 4

# HBNN specific
HBNN_NODES = 15
HBNN_SIG = "015"

# GP specific
GP_N_INDUCING_MEAN = 100
GP_N_INDUCING_VAR = 50
#######################################################################################

os.makedirs('Dataset_D_training_with_Xiong', exist_ok=True)

df_train = get_dataset('Datasets/database_D_old_format.txt', 'MS')
df_train = df_train[df_train['mode'] == 'A']

# Unpack all 8 arrays. Note: return_train_test currently returns radius as the target.
(x_train, x_train_er, x_test, x_test_err, rad_train, erad_train,
 rad_test, erad_test
) = return_train_test(df_train)

if TARGET_VAR == "radius":
    y_train, ey_train = rad_train, erad_train
    y_test, ey_test = rad_test, erad_test
elif TARGET_VAR == "mass":
    mtmass = df_train['M'].mean()
    stmass = df_train['M'].std(ddof=0)
    
    y_train = (df_train.loc[x_train.index, 'M'] - mtmass) / stmass
    ey_train = abs((df_train.loc[x_train.index, 'eM1'] + df_train.loc[x_train.index, 'eM2']) / 2) / stmass
    y_test = (df_train.loc[x_test.index, 'M'] - mtmass) / stmass
    ey_test = abs((df_train.loc[x_test.index, 'eM1'] + df_train.loc[x_test.index, 'eM2']) / 2) / stmass
else:
    raise ValueError("TARGET_VAR must be 'radius' or 'mass'")

unorm_y = denormalise_val(y_test, TARGET_VAR)

x_train = x_train[['Teff', 'logg', 'Meta', 'L']]
x_train_er = x_train_er[['eTeff', 'elogg', 'eMeta', 'eL']]

x_test = x_test[['Teff', 'logg', 'Meta', 'L']]
x_test_er = x_test_err[['eTeff', 'elogg', 'eMeta', 'eL']]


def main():

    print('A-label stars used after cleanup:', len(df_train))
    print('Training stars:', len(x_train))
    print('Test stars:', len(x_test))
    print(f'Active Model: {ACTIVE_MODEL}')
    print(f'Target Variable: {TARGET_VAR}')

    target_abbr = 'rad' if TARGET_VAR == 'radius' else 'mass'

    if ACTIVE_MODEL == "HBNN":
        model_string = f"HBNN_{target_abbr}_4param_L_{DRAWS}_draws_{CHAINS}_chains_{HBNN_NODES}_nodes_sig_{HBNN_SIG}_seed_{SEED}"
        trace_path = f"Dataset_D_training_with_Xiong/{model_string}.nc"
        
        model = hbnn.HBNN_M4(x_train, y_train, x_train_er, ey_train, HBNN_NODES)
        trace = train(model, trace_path, draw=DRAWS, chains=CHAINS)
        
        pred, lpd = sample_post_pred_HBNN_para(trace, x_test, x_test_er, HBNN_NODES, 4, TARGET_VAR)

    elif ACTIVE_MODEL == "GP":
        model_string = f"GP_{target_abbr}_4param_L_{DRAWS}_draws_{CHAINS}_chains_{GP_N_INDUCING_MEAN}_{GP_N_INDUCING_VAR}_seed_{SEED}"
        trace_path = f"Dataset_D_training_with_Xiong/{model_string}.nc"
        
        model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(
            x_train, x_train_er, y_train, GP_N_INDUCING_MEAN, GP_N_INDUCING_VAR)
        trace = train(model, trace_path, draw=DRAWS, chains=CHAINS)
        
        pred, lpd = posterior_predictive_GP(
            model, μ_gp, log_var_gp, trace,
            x_test, x_test_er, Xu, Xu_er, 4, TARGET_VAR
        )
    else:
        raise ValueError("ACTIVE_MODEL must be 'HBNN' or 'GP'")


    r_hat_values = az.rhat(trace)
    all_rhats = []
    for var in r_hat_values.data_vars:
        max_rhat = r_hat_values[var].max().values.item()
        all_rhats.append((var, max_rhat))

    print("R-hats:", all_rhats)
    print(az.loo(trace))
    
    Y_pred_sigma = pred.std(0)
    Y_pred_mean = pred.mean(0)

    print('MAE: ', mean_absolute_error(unorm_y, Y_pred_mean))
    print('MARD', mard(unorm_y, Y_pred_mean))
    print('MRD', mrd(unorm_y, Y_pred_mean))

    original_db = pd.read_table('Datasets/database_D_old_format.txt', sep='\t', comment='%')
    test_original_rows = original_db.loc[x_test.index]
    id_col = 'SIMBAD_ID' if 'SIMBAD_ID' in test_original_rows.columns else 'ID'
    residual_Y = Y_pred_mean - np.asarray(unorm_y)
    
    # Prefix for dataframe columns dynamically adjusting to target
    prefix = 'R' if TARGET_VAR == 'radius' else 'M'
    
    diagnostic_table = pd.DataFrame({
        'original_row': x_test.index,
        'ID': test_original_rows[id_col].values if id_col in test_original_rows.columns else np.nan,
        'catalog': test_original_rows['catalog'].values if 'catalog' in test_original_rows.columns else np.nan,
        f'{prefix}_true': np.asarray(unorm_y),
        f'{prefix}_pred': Y_pred_mean,
        f'{prefix}_pred_sigma': Y_pred_sigma,
        f'residual_{prefix}': residual_Y,
        f'abs_residual_{prefix}': np.abs(residual_Y),
        'relative_error_pct': residual_Y / np.asarray(unorm_y) * 100,
        'abs_relative_error_pct': np.abs(residual_Y / np.asarray(unorm_y) * 100),
        'pull': np.where(Y_pred_sigma != 0, residual_Y / Y_pred_sigma, np.nan),
        'abs_pull': np.abs(np.where(Y_pred_sigma != 0, residual_Y / Y_pred_sigma, np.nan)),
    })
    
    diagnostic_path = f"Dataset_D_training_with_Xiong/{TARGET_VAR}_prediction_results_{ACTIVE_MODEL}_{DRAWS}_seed_{SEED}.tsv"
    diagnostic_table.to_csv(diagnostic_path, sep='\t', index=False)
    
    diagnostic_print_columns = ['original_row', 'ID', 'catalog', f'{prefix}_true', f'{prefix}_pred', f'{prefix}_pred_sigma',
                                f'residual_{prefix}', f'abs_residual_{prefix}', 'relative_error_pct',
                                'abs_relative_error_pct', 'pull', 'abs_pull']

    print(f'\nTop 20 {TARGET_VAR} prediction errors by abs_relative_error_pct:')
    print(diagnostic_table.sort_values('abs_relative_error_pct', ascending=False).head(20).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print(f'\nTop 10 {TARGET_VAR} prediction uncertainties by {prefix}_pred_sigma:')
    print(diagnostic_table.sort_values(f'{prefix}_pred_sigma', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print(f'\nTop 10 {TARGET_VAR} prediction pulls by abs_pull:')
    print(diagnostic_table.sort_values('abs_pull', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    sigma_cut = np.percentile(Y_pred_sigma, 95)
    plot_mask = Y_pred_sigma < sigma_cut
    unorm_y_plot = np.asarray(unorm_y)[plot_mask]
    Y_pred_mean_plot = Y_pred_mean[plot_mask]
    Y_pred_sigma_plot = Y_pred_sigma[plot_mask]
    
    plot_output_base = f"Dataset_D_training_with_Xiong/{model_string}"
    unit = r'$R_\odot$' if TARGET_VAR == 'radius' else r'$M_\odot$'
    cap_target = TARGET_VAR.capitalize()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y, Y_pred_mean, yerr=Y_pred_sigma, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_y.min(), unorm_y.max()], [unorm_y.min(), unorm_y.max()], 'r--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Predicted {cap_target} ({unit})', fontsize=14)
    plt.title(f'{ACTIVE_MODEL} Predictions with Uncertainty')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_full_prediction.png', dpi=300, bbox_inches='tight')
    plt.show() if SHOW_PLOTS else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y, Y_pred_mean - unorm_y, yerr=Y_pred_sigma, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_y.min(), unorm_y.max(), 'r', linestyle='--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Residual {cap_target} ({unit})', fontsize=14)
    plt.title(f'{ACTIVE_MODEL} Predictions with Uncertainty')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_full_residual.png', dpi=300, bbox_inches='tight')
    plt.show() if SHOW_PLOTS else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y_plot, Y_pred_mean_plot, yerr=Y_pred_sigma_plot, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_y_plot.min(), unorm_y_plot.max()], [unorm_y_plot.min(), unorm_y_plot.max()], 'r--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Predicted {cap_target} ({unit})', fontsize=14)
    plt.title(f'{ACTIVE_MODEL} Predictions with Uncertainty ({prefix}_pred_sigma < 95th percentile)')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_filtered_prediction.png', dpi=300, bbox_inches='tight')
    plt.show() if SHOW_PLOTS else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y_plot, Y_pred_mean_plot - unorm_y_plot, yerr=Y_pred_sigma_plot, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_y_plot.min(), unorm_y_plot.max(), 'r', linestyle='--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Residual {cap_target} ({unit})', fontsize=14)
    plt.title(f'{ACTIVE_MODEL} Residual {cap_target} ({prefix}_pred_sigma < 95th percentile)')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_filtered_residual.png', dpi=300, bbox_inches='tight')
    plt.show() if SHOW_PLOTS else plt.close()

if __name__ == '__main__':
    main()