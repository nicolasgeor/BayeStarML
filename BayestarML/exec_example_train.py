#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:50:13 2025

@author: LamirelFamily
"""

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error

from constants import (
    FEATURE_ERRORS,
    FEATURES,
    GP_MASS_TRACE_PATH,
    HBNN_MASS_TRACE_PATH,
    TARGET,
    TRAINING_DATA_FILE,
)
from models import gp, hbnn
from pred_sampling import posterior_predictive_GP, sample_post_pred_HBNN_para
from preprocess import denormalise_val, return_train_test
from utils import get_dataset, mard, mrd, train


# Choose exactly one model to train by commenting/uncommenting these two lines.
TRAIN_MODEL = "gp"
# TRAIN_MODEL = "hbnn"

N_HIDDEN = 15
GP_M_MEAN = 80
GP_M_VAR = 40
DRAWS = 1000
CHAINS = 2
DIAGNOSTIC_OUTPUT_DIR = Path("Dataset_A_training")


df_train = get_dataset(TRAINING_DATA_FILE, "MS", features=FEATURES, target=TARGET)
(
    x_train,
    x_train_er,
    x_test,
    x_test_err,
    mass_train,
    emass_train,
    mass_test,
    emass_test,
) = return_train_test(df_train, target=TARGET)

unorm_mass = denormalise_val(mass_test, TARGET)

x_train = x_train[FEATURES]
x_train_er = x_train_er[FEATURE_ERRORS]
x_test = x_test[FEATURES]
x_test_er = x_test_err[FEATURE_ERRORS]


def build_selected_model():
    if TRAIN_MODEL == "gp":
        model, mu_gp, log_var_gp, Xu, Xu_var = gp.sparse_fully_heteroscedastic_gp(
            x_train,
            x_train_er,
            mass_train,
            GP_M_MEAN,
            GP_M_VAR,
        )
        return model, GP_MASS_TRACE_PATH, {
            "mu_gp": mu_gp,
            "log_var_gp": log_var_gp,
            "Xu": Xu,
            "Xu_var": Xu_var,
        }

    if TRAIN_MODEL == "hbnn":
        model = hbnn.HBNN_M3(
            x_train,
            mass_train,
            x_train_er,
            emass_train,
            N_HIDDEN,
        )
        return model, HBNN_MASS_TRACE_PATH, {}

    raise ValueError('TRAIN_MODEL must be either "gp" or "hbnn".')


def sample_holdout_predictions(model, trace, model_info):
    if TRAIN_MODEL == "gp":
        return posterior_predictive_GP(
            model,
            model_info["mu_gp"],
            model_info["log_var_gp"],
            trace,
            x_test,
            x_test_er,
            model_info["Xu"],
            model_info["Xu_var"],
            len(FEATURES),
            TARGET,
        )

    return sample_post_pred_HBNN_para(
        trace,
        x_test,
        x_test_er,
        N_HIDDEN,
        len(FEATURES),
        TARGET,
    )


def print_diagnostics(trace):
    r_hat_values = az.rhat(trace)
    all_rhats = []
    for var in r_hat_values.data_vars:
        max_rhat = r_hat_values[var].max().values.item()
        all_rhats.append((var, max_rhat))

    print("R-hat values:", all_rhats)
    print(az.loo(trace))


def build_holdout_residual_diagnostics(pred):
    test_index = x_test.index
    pred_mean = np.asarray(pred.mean(0), dtype=float)
    pred_sigma = np.asarray(pred.std(0), dtype=float)

    if len(test_index) != len(pred_mean):
        raise ValueError(
            "Cannot build holdout diagnostics: prediction count "
            f"({len(pred_mean)}) does not match x_test rows ({len(test_index)})."
        )

    source_rows = df_train.loc[test_index]
    if isinstance(unorm_mass, pd.Series):
        true_mass = unorm_mass.reindex(test_index).to_numpy(dtype=float)
    else:
        true_mass = np.asarray(unorm_mass, dtype=float)

    diagnostics = pd.DataFrame({"original_row": test_index}, index=test_index)

    optional_columns = [
        "ID",
        "SIMBAD_ID",
        "source",
        "catalog",
        "Fe/H",
        "Meta",
        "e1_Fe/H",
        "e2_Fe/H",
        "eMeta1",
        "eMeta2",
    ]
    for column in optional_columns:
        if column in source_rows.columns:
            diagnostics[column] = source_rows[column]

    diagnostics["M_true"] = true_mass
    diagnostics["M_pred"] = pred_mean
    diagnostics["M_pred_sigma"] = pred_sigma
    diagnostics["residual_M"] = diagnostics["M_pred"] - diagnostics["M_true"]
    diagnostics["abs_residual_M"] = diagnostics["residual_M"].abs()
    diagnostics["relative_error_pct"] = np.where(
        diagnostics["M_true"] != 0,
        100.0 * diagnostics["residual_M"] / diagnostics["M_true"],
        np.nan,
    )
    diagnostics["abs_relative_error_pct"] = diagnostics["relative_error_pct"].abs()
    diagnostics["pull"] = np.where(
        diagnostics["M_pred_sigma"] != 0,
        diagnostics["residual_M"] / diagnostics["M_pred_sigma"],
        np.nan,
    )
    diagnostics["abs_pull"] = diagnostics["pull"].abs()

    return diagnostics.sort_values("abs_relative_error_pct", ascending=False)


def write_holdout_residual_diagnostics(pred):
    diagnostics = build_holdout_residual_diagnostics(pred)
    DIAGNOSTIC_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = (
        DIAGNOSTIC_OUTPUT_DIR
        / f"{TRAIN_MODEL}_mass_3features_holdout_residual_diagnostics.tsv"
    )
    diagnostics.to_csv(output_path, sep="\t", index=False)
    print(f"Saved holdout residual diagnostics to {output_path}")
    return diagnostics


def print_worst_holdout_rows(diagnostics):
    with pd.option_context("display.max_columns", None, "display.width", 220):
        print("\nTop 40 rows by abs_relative_error_pct:")
        print(diagnostics.head(40).to_string(index=False))

        print("\nTop 25 rows by M_pred_sigma:")
        print(
            diagnostics.sort_values("M_pred_sigma", ascending=False)
            .head(25)
            .to_string(index=False)
        )

        print("\nTop 25 rows by abs_pull:")
        print(
            diagnostics.sort_values("abs_pull", ascending=False)
            .head(25)
            .to_string(index=False)
        )


def plot_holdout(pred):
    true_mass = np.asarray(unorm_mass, dtype=float)
    pred_mean = np.asarray(pred.mean(0), dtype=float)
    pred_sigma = np.asarray(pred.std(0), dtype=float)

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        true_mass,
        pred_mean,
        yerr=pred_sigma,
        fmt="o",
        label="Predictions with Uncertainty",
        alpha=0.7,
    )
    plt.plot(
        [true_mass.min(), true_mass.max()],
        [true_mass.min(), true_mass.max()],
        "r--",
    )
    plt.xlabel("True Mass")
    plt.ylabel("Predicted Mass")
    plt.title(f"{TRAIN_MODEL.upper()} Mass Predictions with Uncertainty")
    plt.legend()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        true_mass,
        pred_mean - true_mass,
        yerr=pred_sigma,
        fmt="o",
        label="Predictions with Uncertainty",
        alpha=0.7,
    )
    plt.hlines(0, true_mass.min(), true_mass.max(), "r", linestyle="--")
    plt.xlabel("True Mass")
    plt.ylabel("Residual Mass")
    plt.legend()
    plt.show()

    sigma_p95 = np.nanpercentile(pred_sigma, 95)
    sigma_mask = np.isfinite(pred_sigma) & (pred_sigma < sigma_p95)
    print(
        f"Plotting {sigma_mask.sum()}/{len(pred_sigma)} holdout rows with "
        f"M_pred_sigma below the 95th percentile ({sigma_p95:.6g})."
    )
    if not sigma_mask.any():
        print("Skipped filtered uncertainty plot because no finite rows passed the filter.")
        return

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        true_mass[sigma_mask],
        pred_mean[sigma_mask],
        yerr=pred_sigma[sigma_mask],
        fmt="o",
        label="Below 95th Percentile Uncertainty",
        alpha=0.7,
    )
    plt.plot(
        [true_mass[sigma_mask].min(), true_mass[sigma_mask].max()],
        [true_mass[sigma_mask].min(), true_mass[sigma_mask].max()],
        "r--",
    )
    plt.xlabel("True Mass")
    plt.ylabel("Predicted Mass")
    plt.title(
        f"{TRAIN_MODEL.upper()} Mass Predictions "
        "(M_pred_sigma < 95th Percentile)"
    )
    plt.legend()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        true_mass[sigma_mask],
        pred_mean[sigma_mask] - true_mass[sigma_mask],
        yerr=pred_sigma[sigma_mask],
        fmt="o",
        label="Below 95th Percentile Uncertainty",
        alpha=0.7,
    )
    plt.hlines(
        0,
        true_mass[sigma_mask].min(),
        true_mass[sigma_mask].max(),
        "r",
        linestyle="--",
    )
    plt.xlabel("True Mass")
    plt.ylabel("Residual Mass")
    plt.title(
        f"{TRAIN_MODEL.upper()} Residuals "
        "(M_pred_sigma < 95th Percentile)"
    )
    plt.legend()
    plt.show()


def main():
    model, output_path, model_info = build_selected_model()

    trace = train(model, output_path, draw=DRAWS, chains=CHAINS)
    print(f"Saved {TRAIN_MODEL.upper()} trace to {output_path}")

    print_diagnostics(trace)

    pred, lpd = sample_holdout_predictions(model, trace, model_info)

    print(pred.std(0))
    print(pred.mean(0))
    print(unorm_mass)

    print("MAE:", mean_absolute_error(unorm_mass, pred.mean(0)))
    print("MARD:", mard(unorm_mass, pred.mean(0)))
    print("MRD:", mrd(unorm_mass, pred.mean(0)))
    diagnostics = write_holdout_residual_diagnostics(pred)
    print_worst_holdout_rows(diagnostics)

    plot_holdout(pred)


if __name__ == "__main__":
    main()
