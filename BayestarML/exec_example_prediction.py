#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily

Predict masses or radii for a Dataset-D-format database with the stacked (BHS) 4-feature
model, or evaluate the stack on the holdout set. All settings live in run_pipeline.py.
"""

import os

import numpy as np
import pandas as pd

from preprocess import return_norm, TARGET_COLUMNS
from predict import predict4, print_model_metrics
from utils import get_dataset
import analyse_eb_mass_oblateness_residuals
import analyse_eb_radius_oblateness_residuals


# Extra columns required only for real prediction rows.
REQUIRED_PREDICTION_COLUMNS = [
    "oblateness", "eoblateness1", "eoblateness2",
    "fill_factor", "efill_factor1", "efill_factor2",
]

def prepare_database_d_predictions(cfg):
    """
    Prepare a Dataset-D-format database for 4-feature mass/radius prediction.

    Uses Teff, logg, Meta, and L, with mean asymmetric uncertainties.
    Rows without the required prediction inputs are skipped.
    The database must have the same tab-separated old-format columns as database_D_old_format.txt.
    """
    data = pd.read_table(cfg.prediction_database, sep="\t", comment="%")

    if cfg.prediction_star_class is not None and "class" in data.columns:
        data = data[data["class"] == cfg.prediction_star_class]

    if cfg.prediction_mode is not None and "mode" in data.columns:
        data = data[data["mode"] == cfg.prediction_mode]

    value_cols = ["Teff", "logg", "Meta", "L"]
    lower_error_cols = ["eTeff1", "elogg1", "eMeta1", "eL1"]
    upper_error_cols = ["eTeff2", "elogg2", "eMeta2", "eL2"]
    required_cols = value_cols + lower_error_cols + upper_error_cols + REQUIRED_PREDICTION_COLUMNS

    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        raise ValueError(f"Prediction database is missing columns: {missing_cols}")

    prediction_rows = data.copy()
    for col in required_cols:
        prediction_rows[col] = pd.to_numeric(prediction_rows[col], errors="coerce")

    prediction_rows = prediction_rows.dropna(subset=required_cols).copy()
    if prediction_rows.empty:
        raise ValueError("No rows have all required 4-feature prediction inputs.")

    # Features are normalised with the statistics of the training split the models were trained on
    df_train = get_dataset(cfg.database, "MS")
    df_train = df_train[df_train["mode"] == "A"]
    mteff, mlogg, mmet, mlum, _mtrad, steff, slogg, smet, slum, _srad = return_norm(df_train, random_state=cfg.split_seed)

    x_pred = pd.DataFrame({
        "Teff": (prediction_rows["Teff"] - mteff) / steff,
        "logg": (prediction_rows["logg"] - mlogg) / slogg,
        "Meta": (prediction_rows["Meta"] - mmet) / smet,
        "L": (prediction_rows["L"] - mlum) / slum,
    }, index=prediction_rows.index)

    x_pred_er = pd.DataFrame({
        "eTeff": abs((prediction_rows["eTeff1"] + prediction_rows["eTeff2"]) / 2) / steff,
        "elogg": abs((prediction_rows["elogg1"] + prediction_rows["elogg2"]) / 2) / slogg,
        "eMeta": abs((prediction_rows["eMeta1"] + prediction_rows["eMeta2"]) / 2) / smet,
        "eL": abs((prediction_rows["eL1"] + prediction_rows["eL2"]) / 2) / slum,
    }, index=prediction_rows.index)

    return prediction_rows, x_pred, x_pred_er


def build_prediction_table(prediction_rows, bhs_pred, target):
    # Column names expected by the oblateness analysis scripts: rad_* for radius, mass_* for mass
    prefix = "rad" if target == "radius" else "mass"
    prediction_summary = pd.DataFrame({
        f"{prefix}_pred": bhs_pred.mean(0),
        f"{prefix}_sigma": bhs_pred.std(0),
        f"{prefix}_p16": np.percentile(bhs_pred, 16, axis=0),
        f"{prefix}_p84": np.percentile(bhs_pred, 84, axis=0),
        f"{prefix}_p02_5": np.percentile(bhs_pred, 2.5, axis=0),
        f"{prefix}_p97_5": np.percentile(bhs_pred, 97.5, axis=0),
    }, index=prediction_rows.index)

    return pd.concat(
        [prediction_rows.reset_index(names="original_row"), prediction_summary.reset_index(drop=True)],
        axis=1,
    )


def analysis_selection(prediction_rows, y_true, target):
    """
    Stars kept by the oblateness analysis (the thesis sample): catalogue value inside the analysis
    window, positive oblateness and, if ROBUST, inputs inside the robust feature ranges.
    The cut values are read from the analysis script itself, so both always agree.
    Returns the boolean mask and a short description of the cuts.
    """
    if target == "radius":
        analysis = analyse_eb_radius_oblateness_residuals
        lo, hi, true_col = analysis.RAD_MIN, analysis.RAD_MAX, "R"
    else:
        analysis = analyse_eb_mass_oblateness_residuals
        lo, hi, true_col = analysis.MASS_MIN, analysis.MASS_MAX, "M"

    keep = np.isfinite(y_true) & (y_true >= lo) & (y_true <= hi)
    keep &= (prediction_rows["oblateness"] > analysis.MIN_OBLATENESS).to_numpy()
    description = f"{lo:g} <= {true_col} <= {hi:g}"
    if analysis.ROBUST:
        keep &= analysis.robust_feature_mask(prediction_rows).to_numpy()
        description += ", inputs within the robust feature ranges"
    return keep, description


def run_holdout_evaluation(cfg):
    """Train BART and stack all three models on the built-in holdout set; prints MARD/MRD."""
    print("Evaluating Dataset D A-label 4-parameter BHS on the holdout test set...")
    predict4(None, None, cfg, test=True)
    print("\n--- Evaluation Complete ---")


def run_eb_predictions(cfg):
    """Predict the stars of cfg.prediction_database and save them to cfg.eb_predictions_path."""
    print(f"Preparing 4-feature {cfg.target} predictions for {cfg.prediction_database}...")
    prediction_rows, X, X_er = prepare_database_d_predictions(cfg)

    print(f"Predicting {cfg.target} for {len(prediction_rows)} star(s)...")
    base_preds, bhs_pred, _bhs_w = predict4(X, X_er, cfg, test=False)

    prediction_table = build_prediction_table(prediction_rows, bhs_pred, cfg.target)
    os.makedirs(os.path.dirname(cfg.eb_predictions_path), exist_ok=True)
    prediction_table.to_csv(cfg.eb_predictions_path, index=False)

    prefix = "rad" if cfg.target == "radius" else "mass"
    print(f"Saved predictions to {cfg.eb_predictions_path}")
    print(prediction_table[["original_row", "SIMBAD_ID", f"{prefix}_pred", f"{prefix}_sigma"]].head().to_string(index=False))

    # Results of all 4 models against the catalogue values of the predicted stars
    true_col = TARGET_COLUMNS[cfg.target][0]
    y_true = pd.to_numeric(prediction_rows[true_col], errors="coerce").to_numpy()
    has_true = np.isfinite(y_true)
    stars = f"{cfg.prediction_mode} stars" if cfg.prediction_mode else "predicted stars"
    print(f"\nResults of the 4 models on ALL {has_true.sum()} {stars} with a catalogue {cfg.target} ({true_col}), with NO cuts")
    print("(includes stars outside the training range). NOT comparable to the holdout MARD/MRD/MAE")
    print("of the training and holdout steps, which are measured on asteroseismic test stars:")
    bart_pred, gp_pred, hbnn_pred = base_preds
    model_preds = [("BART", bart_pred), ("GP", gp_pred), ("HBNN", hbnn_pred), ("BHS", bhs_pred)]
    print_model_metrics(y_true[has_true], {name: pred[:, has_true] for name, pred in model_preds})

    # Same metrics on the stars the oblateness analysis keeps (the sample used in the thesis)
    selected, cuts = analysis_selection(prediction_rows, y_true, cfg.target)
    print(f"\nResults of the 4 models on the {selected.sum()} {stars} kept by the oblateness analysis cuts")
    print(f"({cuts}; same selection as the analysis step):")
    if selected.any():
        print_model_metrics(y_true[selected], {name: pred[:, selected] for name, pred in model_preds})
    else:
        print("No stars pass the analysis cuts.")
    print("\n--- Prediction Complete ---")


if __name__ == '__main__':
    # Settings live in run_pipeline.py. Running this file only does the prediction steps
    # switched on there (RUN_HOLDOUT_EVAL / RUN_PREDICT).
    import run_pipeline
    run_pipeline.main(only=("holdout_eval", "predict"))
