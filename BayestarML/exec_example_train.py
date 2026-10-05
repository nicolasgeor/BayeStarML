#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:50:13 2025

@author: LamirelFamily

Train the GP or the HBNN on the Dataset D asteroseismic (mode A) stars and evaluate it
on the holdout set. All settings (seeds, draws, model sizes, paths) live in run_pipeline.py.
"""

from preprocess import return_train_test, denormalise_val
from utils import get_dataset, train, mard, mrd
from models import hbnn, gp
from pred_sampling import sample_post_pred_HBNN_para, posterior_predictive_GP
import arviz as az
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_absolute_error


def train_and_evaluate(cfg, model_name):
    """
    Train one model ("GP" or "HBNN"), save its trace, and evaluate it on the holdout set.

    Writes the trace, a holdout diagnostics TSV and four prediction/residual plots to
    cfg.training_dir, with the file names defined in run_pipeline.RunConfig.
    """
    os.makedirs(cfg.training_dir, exist_ok=True)

    df_train = get_dataset(cfg.database, 'MS')
    df_train = df_train[df_train['mode'] == 'A']

    (x_train, x_train_er, x_test, x_test_err, y_train, ey_train,
     y_test, ey_test
    ) = return_train_test(df_train, target=cfg.target, random_state=cfg.split_seed)

    unorm_y = denormalise_val(y_test, cfg.target)

    x_train = x_train[['Teff', 'logg', 'Meta', 'L']]
    x_train_er = x_train_er[['eTeff', 'elogg', 'eMeta', 'eL']]

    x_test = x_test[['Teff', 'logg', 'Meta', 'L']]
    x_test_er = x_test_err[['eTeff', 'elogg', 'eMeta', 'eL']]

    print('A-label stars used after cleanup:', len(df_train))
    print('Training stars:', len(x_train))
    print('Test stars:', len(x_test))
    print(f'Active Model: {model_name}')
    print(f'Target Variable: {cfg.target}')

    model_string = cfg.model_string(model_name)
    trace_path = cfg.trace_path(model_name)
    # Stored in the trace so the prediction step can check it uses the same train/test split
    trace_attrs = {'split_seed': cfg.split_seed, 'database': cfg.database}

    if model_name == "HBNN":
        model = hbnn.HBNN_M4(x_train, y_train, x_train_er, ey_train, cfg.hbnn_nodes)
        trace = train(model, trace_path, draw=cfg.draws, chains=cfg.chains,
                      random_seed=cfg.seed, attrs=trace_attrs)

        pred, lpd = sample_post_pred_HBNN_para(trace, x_test, x_test_er, cfg.hbnn_nodes, 4, cfg.target,
                                               seed=cfg.seed)

    elif model_name == "GP":
        model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(
            x_train, x_train_er, y_train, cfg.gp_n_inducing_mean, cfg.gp_n_inducing_var)
        trace = train(model, trace_path, draw=cfg.draws, chains=cfg.chains,
                      random_seed=cfg.seed, attrs=trace_attrs)

        pred, lpd = posterior_predictive_GP(
            model, μ_gp, log_var_gp, trace,
            x_test, x_test_er, Xu, Xu_er, 4, cfg.target
        )
    else:
        raise ValueError("model_name must be 'HBNN' or 'GP'")


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

    original_db = pd.read_table(cfg.database, sep='\t', comment='%')
    test_original_rows = original_db.loc[x_test.index]
    id_col = 'SIMBAD_ID' if 'SIMBAD_ID' in test_original_rows.columns else 'ID'
    residual_Y = Y_pred_mean - np.asarray(unorm_y)

    # Prefix for dataframe columns dynamically adjusting to target
    prefix = 'R' if cfg.target == 'radius' else 'M'

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

    diagnostic_path = cfg.test_results_path(model_name)
    diagnostic_table.to_csv(diagnostic_path, sep='\t', index=False)

    diagnostic_print_columns = ['original_row', 'ID', 'catalog', f'{prefix}_true', f'{prefix}_pred', f'{prefix}_pred_sigma',
                                f'residual_{prefix}', f'abs_residual_{prefix}', 'relative_error_pct',
                                'abs_relative_error_pct', 'pull', 'abs_pull']

    print(f'\nTop 20 {cfg.target} prediction errors by abs_relative_error_pct:')
    print(diagnostic_table.sort_values('abs_relative_error_pct', ascending=False).head(20).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print(f'\nTop 10 {cfg.target} prediction uncertainties by {prefix}_pred_sigma:')
    print(diagnostic_table.sort_values(f'{prefix}_pred_sigma', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    print(f'\nTop 10 {cfg.target} prediction pulls by abs_pull:')
    print(diagnostic_table.sort_values('abs_pull', ascending=False).head(10).to_csv(sep='\t', index=False, columns=diagnostic_print_columns).strip())

    sigma_cut = np.percentile(Y_pred_sigma, 95)
    plot_mask = Y_pred_sigma < sigma_cut
    unorm_y_plot = np.asarray(unorm_y)[plot_mask]
    Y_pred_mean_plot = Y_pred_mean[plot_mask]
    Y_pred_sigma_plot = Y_pred_sigma[plot_mask]

    plot_output_base = f"{cfg.training_dir}/{model_string}"
    unit = r'$R_\odot$' if cfg.target == 'radius' else r'$M_\odot$'
    cap_target = cfg.target.capitalize()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y, Y_pred_mean, yerr=Y_pred_sigma, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_y.min(), unorm_y.max()], [unorm_y.min(), unorm_y.max()], 'r--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Predicted {cap_target} ({unit})', fontsize=14)
    plt.title(f'{model_name} Predictions with Uncertainty')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_full_prediction.png', dpi=300, bbox_inches='tight')
    plt.show() if cfg.show_plots else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y, Y_pred_mean - unorm_y, yerr=Y_pred_sigma, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_y.min(), unorm_y.max(), 'r', linestyle='--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Residual {cap_target} ({unit})', fontsize=14)
    plt.title(f'{model_name} Predictions with Uncertainty')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_full_residual.png', dpi=300, bbox_inches='tight')
    plt.show() if cfg.show_plots else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y_plot, Y_pred_mean_plot, yerr=Y_pred_sigma_plot, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_y_plot.min(), unorm_y_plot.max()], [unorm_y_plot.min(), unorm_y_plot.max()], 'r--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Predicted {cap_target} ({unit})', fontsize=14)
    plt.title(f'{model_name} Predictions with Uncertainty ({prefix}_pred_sigma < 95th percentile)')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_filtered_prediction.png', dpi=300, bbox_inches='tight')
    plt.show() if cfg.show_plots else plt.close()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_y_plot, Y_pred_mean_plot - unorm_y_plot, yerr=Y_pred_sigma_plot, fmt='o', color='black', ecolor='blue', markersize=5, label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_y_plot.min(), unorm_y_plot.max(), 'r', linestyle='--')
    plt.xlabel(f'True {cap_target} ({unit})', fontsize=14)
    plt.ylabel(f'Residual {cap_target} ({unit})', fontsize=14)
    plt.title(f'{model_name} Residual {cap_target} ({prefix}_pred_sigma < 95th percentile)')
    plt.legend(fontsize=12)
    plt.savefig(plot_output_base + '_filtered_residual.png', dpi=300, bbox_inches='tight')
    plt.show() if cfg.show_plots else plt.close()


if __name__ == '__main__':
    # Settings live in run_pipeline.py. Running this file only does the training steps
    # switched on there (RUN_TRAIN_GP / RUN_TRAIN_HBNN).
    import run_pipeline
    run_pipeline.main(only=("train_gp", "train_hbnn"))
