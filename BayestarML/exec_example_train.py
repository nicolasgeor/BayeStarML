#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:50:13 2025

@author: LamirelFamily
"""

import arviz as az
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

from constants import (
    DATASET_PATH,
    FEATURE_ERRORS,
    FEATURES,
    GP_MASS_TRACE_PATH,
    HBNN_MASS_TRACE_PATH,
    TARGET,
)
from models import gp, hbnn
from pred_sampling import posterior_predictive_GP, sample_post_pred_HBNN_para
from preprocess import denormalise_val, return_train_test
from utils import get_dataset, mard, mrd, train


# Choose exactly one model to train by commenting/uncommenting these two lines.
# TRAIN_MODEL = "gp"
TRAIN_MODEL = "hbnn"

N_HIDDEN = 15
GP_M_MEAN = 80
GP_M_VAR = 40
DRAWS = 1000
CHAINS = 2


df_train = get_dataset(DATASET_PATH, "MS")
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


def plot_holdout(pred):
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        unorm_mass,
        pred.mean(0),
        yerr=pred.std(0),
        fmt="o",
        label="Predictions with Uncertainty",
        alpha=0.7,
    )
    plt.plot(
        [unorm_mass.min(), unorm_mass.max()],
        [unorm_mass.min(), unorm_mass.max()],
        "r--",
    )
    plt.xlabel("True Mass")
    plt.ylabel("Predicted Mass")
    plt.title(f"{TRAIN_MODEL.upper()} Mass Predictions with Uncertainty")
    plt.legend()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        unorm_mass,
        pred.mean(0) - unorm_mass,
        yerr=pred.std(0),
        fmt="o",
        label="Predictions with Uncertainty",
        alpha=0.7,
    )
    plt.hlines(0, unorm_mass.min(), unorm_mass.max(), "r", linestyle="--")
    plt.xlabel("True Mass")
    plt.ylabel("Residual Mass")
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

    plot_holdout(pred)


if __name__ == "__main__":
    main()
