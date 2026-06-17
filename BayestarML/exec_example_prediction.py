#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily
"""

import os

import arviz as az
import matplotlib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

matplotlib.use("Agg")

from bhs import run_stack
from models import bart, gp
from pred_sampling import (
    posterior_predictive_GP,
    sample_post_pred_HBNN_para,
    sample_pred_BART,
)
import matplotlib.pyplot as plt
from preprocess import denormalise_val, return_train_test
from utils import get_dataset, mard, mrd


OUTPUT_DIR = "Dataset_B_training_for_Ariel"
TRAINING_FILE = "Datasets/database_B.txt"

GP_TRACE_FILE = os.path.join(
    OUTPUT_DIR, "GP_mass_3param_L_3000_draws_4_chains_100_50_seed_176.nc"
)
HBNN_TRACE_FILE = os.path.join(
    OUTPUT_DIR, "HBNN_mass_3param_L_3000_draws_4_chains_15_nodes_sig_015_seed_176.nc"
)
BART_TRACE_FILE = os.path.join(
    OUTPUT_DIR, "BART_mass_3param_L_holdout_30_draws_4_chains_seed_176.nc"
)
BART_PREDICTIONS_FILE = os.path.join(
    OUTPUT_DIR, "BART_mass_3param_L_holdout_3000_draws_4_chains_predictions_seed_176.nc"
)
BHS_TRACE_FILE = os.path.join(
    OUTPUT_DIR, "BHS_mass_3param_L_holdout_3000_draws_4_chains_seed_176.nc"
)
HOLDOUT_RESULTS_FILE = os.path.join(
    OUTPUT_DIR, "mass_prediction_results_holdout_all_models_seed_176.tsv"
)
MASS_AXIS_LIMITS = (0.4, 2.0)
PLOT_BLUE = "#2563EB"
AXIS_LABEL_SIZE = 20
TICK_LABEL_SIZE = 16
LEGEND_SIZE = 16


def _metrics(y_true, pred_draws):
    pred_mean = pred_draws.mean(0)
    return {
        "MAE": mean_absolute_error(y_true, pred_mean),
        "MARD": mard(y_true, pred_mean),
        "MRD": mrd(y_true, pred_mean),
    }


def _print_metrics_table(metrics_by_model):
    print("\nHoldout metrics")
    print("Model\tMAE\tMARD\tMRD")
    for model_name, values in metrics_by_model.items():
        print(
            f"{model_name}\t"
            f"{values['MAE']:.6f}\t"
            f"{values['MARD']:.6f}\t"
            f"{values['MRD']:.6f}"
        )


def _add_prediction_columns(results, model_name, y_true, pred_draws):
    pred_mean = pred_draws.mean(0)
    pred_sigma = pred_draws.std(0)
    residual = pred_mean - y_true

    results[f"{model_name}_pred"] = pred_mean
    results[f"{model_name}_pred_sigma"] = pred_sigma
    results[f"{model_name}_residual_M"] = residual
    results[f"{model_name}_abs_residual_M"] = np.abs(residual)
    results[f"{model_name}_relative_error_pct"] = residual / y_true * 100
    results[f"{model_name}_abs_relative_error_pct"] = np.abs(residual / y_true * 100)
    results[f"{model_name}_pull"] = np.where(pred_sigma != 0, residual / pred_sigma, np.nan)
    results[f"{model_name}_abs_pull"] = np.abs(results[f"{model_name}_pull"])


def _holdout_metadata(x_test):
    original_db = pd.read_table(TRAINING_FILE, sep="\t", comment="%")
    test_original_rows = original_db.loc[x_test.index]
    id_col = "SIMBAD_ID" if "SIMBAD_ID" in test_original_rows.columns else "ID"

    return pd.DataFrame(
        {
            "original_row": x_test.index,
            "ID": (
                test_original_rows[id_col].values
                if id_col in test_original_rows.columns
                else np.nan
            ),
            "catalog": (
                test_original_rows["catalog"].values
                if "catalog" in test_original_rows.columns
                else np.nan
            ),
        }
    )


def _style_mass_axis(ax, ylabel):
    ax.set_xlim(*MASS_AXIS_LIMITS)
    ax.set_xlabel("True Mass", fontsize=AXIS_LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE)
    ax.tick_params(axis="both", labelsize=TICK_LABEL_SIZE)
    ax.legend(fontsize=LEGEND_SIZE, loc="upper left", frameon=True)


def _plot_prediction(y_true, pred_mean, pred_sigma, output_file):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(
        y_true,
        pred_mean,
        yerr=pred_sigma,
        fmt="o",
        color="black",
        markerfacecolor="black",
        markeredgecolor="black",
        ecolor=PLOT_BLUE,
        elinewidth=1.5,
        alpha=0.75,
        label="Predictions with Uncertainty",
    )
    ax.plot(MASS_AXIS_LIMITS, MASS_AXIS_LIMITS, "r--", linewidth=1.7)
    ax.set_ylim(*MASS_AXIS_LIMITS)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    ax.set_yticks(np.arange(0.4, 2.01, 0.2))
    _style_mass_axis(ax, "Predicted Mass")
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_residual(y_true, pred_mean, pred_sigma, output_file):
    residual = pred_mean - y_true
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(
        y_true,
        residual,
        yerr=pred_sigma,
        fmt="o",
        color="black",
        markerfacecolor="black",
        markeredgecolor="black",
        ecolor=PLOT_BLUE,
        elinewidth=1.5,
        alpha=0.75,
        label="Predictions with Uncertainty",
    )
    ax.hlines(0, *MASS_AXIS_LIMITS, colors="red", linestyles="--", linewidth=1.7)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    spread = np.nanmax(np.abs(residual) + pred_sigma)
    spread = max(0.25, float(spread) * 1.1)
    ax.set_ylim(-spread, spread)
    _style_mass_axis(ax, "Residual Mass")
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_holdout_diagnostics(y_true, pred_draws, output_base, filtered_percentile=95):
    os.makedirs(os.path.dirname(output_base), exist_ok=True)

    pred_mean = pred_draws.mean(0)
    pred_sigma = pred_draws.std(0)
    y_true = np.asarray(y_true)

    _plot_prediction(
        y_true,
        pred_mean,
        pred_sigma,
        output_base + "_full_prediction.png",
    )
    _plot_residual(
        y_true,
        pred_mean,
        pred_sigma,
        output_base + "_full_residual.png",
    )

    sigma_cut = np.percentile(pred_sigma, filtered_percentile)
    plot_mask = pred_sigma <= sigma_cut
    _plot_prediction(
        y_true[plot_mask],
        pred_mean[plot_mask],
        pred_sigma[plot_mask],
        output_base + f"_filtered_{filtered_percentile}_prediction.png",
    )
    _plot_residual(
        y_true[plot_mask],
        pred_mean[plot_mask],
        pred_sigma[plot_mask],
        output_base + f"_filtered_{filtered_percentile}_residual.png",
    )


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df_train = get_dataset(TRAINING_FILE, "MS")
    (
        x_train,
        x_train_er,
        x_test,
        x_test_err,
        mass_train,
        emass_train,
        mass_test,
        emass_test,
    ) = return_train_test(df_train)

    unorm_mass = np.asarray(denormalise_val(mass_test, "mass"))

    x_train = x_train[["Teff", "Meta", "L"]]
    x_train_er = x_train_er[["eTeff", "eMeta", "eL"]]
    X = x_test[["Teff", "Meta", "L"]]
    X_er = x_test_err[["eTeff", "eMeta", "eL"]]

    bart_model = bart.BART_M(x_train, x_train_er, mass_train, emass_train)
    bart_pred, lpd_BART = sample_pred_BART(
        bart_model,
        X,
        X_er,
        "mass",
        3000,
        4,
        trace_filename=BART_TRACE_FILE,
        predictions_filename=BART_PREDICTIONS_FILE,
    )

    gp_model, mu_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(
        x_train, x_train_er, mass_train, 100, 50
    )
    gp_trace = az.from_netcdf(GP_TRACE_FILE)
    gp_pred, lpd_GP = posterior_predictive_GP(
        gp_model, mu_gp, log_var_gp, gp_trace, X, X_er, Xu, Xu_er, 3, "mass"
    )

    hbnn_trace = az.from_netcdf(HBNN_TRACE_FILE)
    hbnn_pred, lpd_HBNN = sample_post_pred_HBNN_para(
        hbnn_trace, X, X_er, 15, 3, "mass"
    )

    bhs_trace, bhs_pred, bhs_w = run_stack(
        bart_pred,
        hbnn_pred,
        gp_pred,
        x_train,
        X,
        lpd_BART,
        lpd_HBNN,
        lpd_GP,
        draws=3000,
        chains=4,
    )
    bhs_trace.to_netcdf(BHS_TRACE_FILE)

    predictions_by_model = {
        "BART": bart_pred,
        "GP": gp_pred,
        "HBNN": hbnn_pred,
        "BHS": bhs_pred,
    }
    metrics_by_model = {
        model_name: _metrics(unorm_mass, pred_draws)
        for model_name, pred_draws in predictions_by_model.items()
    }
    _print_metrics_table(metrics_by_model)

    results = _holdout_metadata(X)
    results["M_true"] = unorm_mass
    for model_name, pred_draws in predictions_by_model.items():
        _add_prediction_columns(results, model_name, unorm_mass, pred_draws)
    results.to_csv(HOLDOUT_RESULTS_FILE, sep="\t", index=False)

    for model_name, pred_draws in predictions_by_model.items():
        _plot_holdout_diagnostics(
            unorm_mass,
            pred_draws,
            os.path.join(
                OUTPUT_DIR, f"{model_name}_mass_3param_L_holdout_seed_176"
            ),
        )

    print("\nSaved holdout results to", HOLDOUT_RESULTS_FILE)


if __name__ == "__main__":
    main()
