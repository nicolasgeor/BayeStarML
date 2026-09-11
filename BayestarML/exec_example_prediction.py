##############################
### I BELIVE THAT IN THIS FILE WE COMMENT/UNCOMMENT TO SWITCH BETWEEN MASS AND RADIUS TRAINING
#################################33

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 18:53:33 2025

@author: LamirelFamily
"""

import os

import numpy as np
import pandas as pd

from preprocess import return_norm
from predict import predict4
from utils import get_dataset


# False: original behavior, evaluate the built-in 20% holdout test set.
# True: predict masses for PREDICTION_DATABASE and save a CSV.
REAL_PREDICTION = True

# Change this path to the database you want to predict.
# It must have the same tab-separated old-format columns as database_D_old_format.txt.
PREDICTION_DATABASE = "Datasets/database_D_old_format.txt"

# Prediction results will be saved here.
# PREDICTION_OUTPUT = "Dataset_D_predictions/EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_82.csv"
PREDICTION_OUTPUT = "Dataset_D_predictions/EB_oblateness_fill_factor_radius_predictions_4_features_100_draws_seed_28.csv"

# Optional filters for the prediction database.
# Leave as None to predict every row that has Teff, logg, Meta, L, and their errors.
PREDICTION_STAR_CLASS = None # e.g. "MS", "RGB", or None for all classes
PREDICTION_MODE = "EB" # e.g. "A", "EB", or None for all modes

# Extra columns required only for real prediction rows.
REQUIRED_PREDICTION_COLUMNS = [
    "oblateness", "eoblateness1", "eoblateness2",
    "fill_factor", "efill_factor1", "efill_factor2",
]

def prepare_database_d_predictions(filename):
    """
    Prepare a Dataset-D-format database for 4-feature mass/radius prediction.

    Uses Teff, logg, Meta, and L, with mean asymmetric uncertainties.
    Rows without the required prediction inputs are skipped.
    """
    data = pd.read_table(filename, sep="\t", comment="%")

    if PREDICTION_STAR_CLASS is not None and "class" in data.columns:
        data = data[data["class"] == PREDICTION_STAR_CLASS]

    if PREDICTION_MODE is not None and "mode" in data.columns:
        data = data[data["mode"] == PREDICTION_MODE]

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

    df_train = get_dataset("Datasets/database_D_old_format.txt", "MS")
    df_train = df_train[df_train["mode"] == "A"]
    # mteff, mlogg, mmet, mlum, _mtmass, steff, slogg, smet, slum, _smass = return_norm(df_train)
    mteff, mlogg, mmet, mlum, _mtrad, steff, slogg, smet, slum, _srad = return_norm(df_train)

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


def build_prediction_table(prediction_rows, bhs_pred):
    prediction_summary = pd.DataFrame({
        # "mass_pred": bhs_pred.mean(0),
        # "mass_sigma": bhs_pred.std(0),
        # "mass_p16": np.percentile(bhs_pred, 16, axis=0),
        # "mass_p84": np.percentile(bhs_pred, 84, axis=0),
        # "mass_p02_5": np.percentile(bhs_pred, 2.5, axis=0),
        # "mass_p97_5": np.percentile(bhs_pred, 97.5, axis=0),
        "rad_pred": bhs_pred.mean(0),
        "rad_sigma": bhs_pred.std(0),
        "rad_p16": np.percentile(bhs_pred, 16, axis=0),
        "rad_p84": np.percentile(bhs_pred, 84, axis=0),
        "rad_p02_5": np.percentile(bhs_pred, 2.5, axis=0),
        "rad_p97_5": np.percentile(bhs_pred, 97.5, axis=0),
    }, index=prediction_rows.index)

    return pd.concat(
        [prediction_rows.reset_index(names="original_row"), prediction_summary.reset_index(drop=True)],
        axis=1,
    )



def main():
    if not REAL_PREDICTION:
        print("Evaluating Dataset D A-label 4-parameter BHS on 20% holdout test set...")
        # _base_preds, _bhs_pred_test, _bhs_w_test = predict4(None, None, "mass", test=True)
        _base_preds, _bhs_pred_test, _bhs_w_test = predict4(None, None, "radius", test=True)
        print("\n--- Evaluation Complete ---")
        return

    # print(f"Preparing 4-feature mass predictions for {PREDICTION_DATABASE}...")
    print(f"Preparing 4-feature radius predictions for {PREDICTION_DATABASE}...")
    prediction_rows, X, X_er = prepare_database_d_predictions(PREDICTION_DATABASE)

    # print(f"Predicting masses for {len(prediction_rows)} star(s)...")
    # _base_preds, bhs_pred, _bhs_w = predict4(X, X_er, "mass", test=False)
    print(f"Predicting radii for {len(prediction_rows)} star(s)...")
    _base_preds, bhs_pred, _bhs_w = predict4(X, X_er, "radius", test=False)

    prediction_table = build_prediction_table(prediction_rows, bhs_pred)
    os.makedirs(os.path.dirname(PREDICTION_OUTPUT), exist_ok=True)
    prediction_table.to_csv(PREDICTION_OUTPUT, index=False)

    print(f"Saved predictions to {PREDICTION_OUTPUT}")
    # print(prediction_table[["original_row", "SIMBAD_ID", "mass_pred", "mass_sigma"]].head().to_string(index=False))
    print(prediction_table[["original_row", "SIMBAD_ID", "rad_pred", "rad_sigma"]].head().to_string(index=False))
    print("\n--- Prediction Complete ---")

    
if __name__ == '__main__':
    main()
