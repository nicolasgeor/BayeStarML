#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:52:30 2025

@author: LamirelFamily
"""

from pathlib import Path

import arviz as az
import numpy as np
import pandas as pd

from bhs import run_stack
from constants import (
    FEATURE_ERRORS,
    FEATURES,
    GP_MASS_TRACE_PATH,
    HBNN_MASS_TRACE_PATH,
    TARGET,
)
from models import bart, gp
from pred_sampling import (
    posterior_predictive_GP,
    sample_post_pred_HBNN_para,
    sample_pred_BART,
)
from preprocess import denormalise_val, return_train_test
from utils import get_dataset, mard, mrd


def _check_mass_target(target):
    if target != TARGET:
        raise NotImplementedError(
            f"This repository is now configured for target={TARGET!r}. "
            f"Got target={target!r}."
        )


def _select_columns(data, columns, name):
    if data is None:
        raise ValueError(f"{name} cannot be None unless test=True.")

    if hasattr(data, "loc"):
        missing = [col for col in columns if col not in data.columns]
        if missing:
            raise ValueError(f"{name} is missing columns {missing}. Required columns: {columns}.")
        return data.loc[:, columns]

    arr = np.asarray(data, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != len(columns):
        raise ValueError(f"{name} must have shape (n_samples, {len(columns)}). Got {arr.shape}.")
    return pd.DataFrame(arr, columns=columns)


def _load_trace(path, model_name):
    trace_path = Path(path)
    if not trace_path.exists():
        raise FileNotFoundError(
            f"{model_name} trace was not found at {trace_path}. "
            "Retrain the model first so the saved trace matches the current "
            "Mass + Teff/Meta/rho configuration."
        )
    return az.from_netcdf(trace_path)


def _print_holdout_metrics(unorm_mass, bart_pred, gp_pred, hbnn_pred, bhs_pred):
    print("MARD BART:", mard(unorm_mass, bart_pred.mean(0)))
    print("MRD BART:", mrd(unorm_mass, bart_pred.mean(0)))

    print("MARD GP:", mard(unorm_mass, gp_pred.mean(0)))
    print("MRD GP:", mrd(unorm_mass, gp_pred.mean(0)))

    print("MARD HBNN:", mard(unorm_mass, hbnn_pred.mean(0)))
    print("MRD HBNN:", mrd(unorm_mass, hbnn_pred.mean(0)))

    print("MARD BHS:", mard(unorm_mass, bhs_pred.mean(0)))
    print("MRD BHS:", mrd(unorm_mass, bhs_pred.mean(0)))


def predict4(X, X_er, target=TARGET, test=False):
    raise NotImplementedError(
        "predict4 is disabled. The active thesis workflow is predict3 with "
        "Mass as target and inputs Teff, Meta, and rho."
    )


def predictNAN(X, X_er, target=TARGET, test=False):
    raise NotImplementedError(
        "predictNAN used the old 4-feature HBNN trace path. Use predict3 for "
        "the current Mass + Teff/Meta/rho workflow."
    )


def predict3(X, X_er, target=TARGET, test=False):
    _check_mass_target(target)

    gp_trace_path = Path(GP_MASS_TRACE_PATH)
    hbnn_trace_path = Path(HBNN_MASS_TRACE_PATH)
    if not gp_trace_path.exists():
        raise FileNotFoundError(
            f"GP trace was not found at {gp_trace_path}. Run exec_example_train.py "
            "after these changes to create a GP trace with the current variance "
            "feature setup."
        )
    if not hbnn_trace_path.exists():
        raise FileNotFoundError(
            f"HBNN trace was not found at {hbnn_trace_path}. Retrain the HBNN "
            "before running stacked predictions."
        )

    df_train = get_dataset("Datasets/data_sample_calculated_density.txt", "MS")
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

    x_train3 = x_train.loc[:, FEATURES]
    x_train3_er = x_train_er.loc[:, FEATURE_ERRORS]

    if test:
        X_pred = x_test.loc[:, FEATURES]
        X_er_pred = x_test_err.loc[:, FEATURE_ERRORS]
    else:
        X_pred = _select_columns(X, FEATURES, "X")
        X_er_pred = _select_columns(X_er, FEATURE_ERRORS, "X_er")

    unorm_mass = denormalise_val(mass_test, TARGET)

    bart3_model = bart.BART_M(
        x_train3,
        x_train3_er,
        mass_train,
        emass_train,
    )
    bart3_pred, lpd_BART3 = sample_pred_BART(
        bart3_model,
        X_pred,
        X_er_pred,
        TARGET,
        draws=2000,
        chains=4,
    )

    gp3_model, mu_gp3, log_var_gp3, Xu3, Xu_var3 = gp.sparse_fully_heteroscedastic_gp(
        x_train3,
        x_train3_er,
        mass_train,
        80,
        40,
    )
    gp3_trace = _load_trace(gp_trace_path, "GP Mass")
    gp3_pred, lpd_GP3 = posterior_predictive_GP(
        gp3_model,
        mu_gp3,
        log_var_gp3,
        gp3_trace,
        X_pred,
        X_er_pred,
        Xu3,
        Xu_var3,
        len(FEATURES),
        TARGET,
    )

    hbnn3_trace = _load_trace(hbnn_trace_path, "HBNN Mass")
    hbnn3_pred, lpd_HBNN3 = sample_post_pred_HBNN_para(
        hbnn3_trace,
        X_pred,
        X_er_pred,
        15,
        len(FEATURES),
        TARGET,
    )

    _, bhs_pred, bhs_w = run_stack(
        bart3_pred,
        hbnn3_pred,
        gp3_pred,
        x_train3,
        X_pred,
        lpd_BART3,
        lpd_HBNN3,
        lpd_GP3,
    )

    if test:
        _print_holdout_metrics(unorm_mass, bart3_pred, gp3_pred, hbnn3_pred, bhs_pred)

    return [bart3_pred, gp3_pred, hbnn3_pred], bhs_pred, bhs_w


def main():
    _, bhs_pred, bhs_w = predict3(None, None, TARGET, test=True)

    Path("Results").mkdir(exist_ok=True)
    pd.DataFrame(bhs_pred.mean(0)).to_csv(
        "Results/3_features_post_pred_bhs_6col_mass_res.csv",
        index=False,
    )
    pd.DataFrame(bhs_w.mean(0)).to_csv(
        "Results/3_features_post_pred_bhs_6col_mass_w.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
