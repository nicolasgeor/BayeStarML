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
from matplotlib.lines import Line2D
from sklearn.metrics import mean_absolute_error

MASS_AXIS_LIMITS = (0.4, 2.0)
PLOT_BLUE = '#2563EB'
AXIS_LABEL_SIZE = 20
TICK_LABEL_SIZE = 16
LEGEND_SIZE = 16

os.makedirs('Dataset_B_training_for_Ariel', exist_ok=True)

df_train = get_dataset('Datasets/database_B.txt', 'MS')
(x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
  mass_test, emass_test
) = return_train_test(df_train)

unorm_mass = denormalise_val(mass_test, 'mass')

x_train = x_train[['Teff', 'Meta', 'L']]
x_train_er = x_train_er[['eTeff', 'eMeta', 'eL']]

x_test = x_test[['Teff', 'Meta', 'L']]
x_test_er = x_test_err[['eTeff', 'eMeta', 'eL']]

# print(x_test3_er)

def _style_mass_axis(ax, ylabel):
    ax.set_xlim(*MASS_AXIS_LIMITS)
    ax.set_xlabel('True Mass', fontsize=AXIS_LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE)
    ax.tick_params(axis='both', labelsize=TICK_LABEL_SIZE)
    legend_handle = Line2D(
        [0], [0],
        marker='o',
        color=PLOT_BLUE,
        markerfacecolor='black',
        markeredgecolor='black',
        linestyle='-',
        linewidth=1.5,
    )
    ax.legend(
        [legend_handle],
        ['Predictions with Uncertainty'],
        fontsize=LEGEND_SIZE,
        loc='upper left',
        frameon=True,
    )


def _plot_prediction(unorm_mass_values, pred_mean, pred_sigma, output_file):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(unorm_mass_values, pred_mean, yerr=pred_sigma, fmt='o',
                color='black', markerfacecolor='black', markeredgecolor='black',
                ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
    ax.plot(MASS_AXIS_LIMITS, MASS_AXIS_LIMITS, 'r--', linewidth=1.7)
    ax.set_ylim(*MASS_AXIS_LIMITS)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    ax.set_yticks(np.arange(0.4, 2.01, 0.2))
    _style_mass_axis(ax, 'Predicted Mass')
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def _plot_residual(unorm_mass_values, pred_mean, pred_sigma, output_file):
    residual = pred_mean - unorm_mass_values
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(unorm_mass_values, residual, yerr=pred_sigma, fmt='o',
                color='black', markerfacecolor='black', markeredgecolor='black',
                ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
    ax.hlines(0, *MASS_AXIS_LIMITS, colors='red', linestyles='--', linewidth=1.7)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    spread = np.nanmax(np.abs(residual) + pred_sigma)
    spread = max(0.25, float(spread) * 1.1)
    ax.set_ylim(-spread, spread)
    _style_mass_axis(ax, 'Residual Mass')
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()
    plt.close(fig)


def _plot_train_diagnostics(unorm_mass_values, pred_mean, pred_sigma, output_base):
    unorm_mass_values = np.asarray(unorm_mass_values)

    _plot_prediction(
        unorm_mass_values,
        pred_mean,
        pred_sigma,
        output_base + '_full_prediction.png',
    )
    _plot_residual(
        unorm_mass_values,
        pred_mean,
        pred_sigma,
        output_base + '_full_residual.png',
    )

    sigma_cut = np.percentile(pred_sigma, 95)
    plot_mask = pred_sigma <= sigma_cut
    _plot_prediction(
        unorm_mass_values[plot_mask],
        pred_mean[plot_mask],
        pred_sigma[plot_mask],
        output_base + '_filtered_prediction.png',
    )
    _plot_residual(
        unorm_mass_values[plot_mask],
        pred_mean[plot_mask],
        pred_sigma[plot_mask],
        output_base + '_filtered_residual.png',
    )


def main():


    # PiCK ONE OF THESE TWO COMBINATiONS (model + trace)
 
    # model = hbnn.HBNN_M3(x_train, mass_train, x_train_er, emass_train, 15)

    
    # trace = train(model, "Dataset_B_training_for_Ariel/HBNN_mass_3param_L_1000_draws_4_chains_15_nodes_sig_015_seed_176.nc", draw=1000, chains=4)

    
    model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(x_train,
                                                                        x_train_er,
                                                                        mass_train, 80, 40)
    
    trace = train(model, "Dataset_B_training_for_Ariel/GP_mass_3param_L_1000_draws_4_chains_80_40_seed_176.nc", draw=1000, chains=4)

    
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
    diagnostic_table.to_csv('Dataset_B_training_for_Ariel/mass_prediction_results_GP_1000_seed_176.tsv', sep='\t', index=False)
    diagnostic_print_columns = ['original_row', 'ID', 'catalog', 'M_true', 'M_pred', 'M_pred_sigma',
                                'residual_M', 'abs_residual_M', 'relative_error_pct',
                                'abs_relative_error_pct', 'pull', 'abs_pull']

    print('\nTop 20 mass prediction errors by abs_relative_error_pct:')
    print(diagnostic_table.sort_values('abs_relative_error_pct', ascending=False).head(20).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 mass prediction uncertainties by M_pred_sigma:')
    print(diagnostic_table.sort_values('M_pred_sigma', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print('\nTop 10 mass prediction pulls by abs_pull:')
    print(diagnostic_table.sort_values('abs_pull', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    plot_output_base = 'Dataset_B_training_for_Ariel/GP_mass_3param_L_1000_draws_4_chains_100_seed_176'
    # plot_output_base = 'Dataset_B_training_for_Ariel/HBNN_mass_3param_L_1000_draws_4_chains_15_nodes_sig_015_seed_176'

    _plot_train_diagnostics(
        unorm_mass,
        M_pred_mean,
        M_pred_sigma,
        plot_output_base,
    )

if __name__ == '__main__':
    main()
