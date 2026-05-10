#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 17:55:32 2025

@author: LamirelFamily
"""

TARGET = "mass"
TRAINING_DATA_FILE = "Datasets/old_database.txt"
PREDICTION_OUTPUT_DIR = "Dataset_A_outputs"

# Canonical 3-input model feature set:
# effective temperature, metallicity, and stellar density.
FEATURES = ["Teff", "Meta", "rho"]
FEATURE_ERRORS = ["eTeff", "eMeta", "erho"]
FEATURE_ERROR_BY_FEATURE = dict(zip(FEATURES, FEATURE_ERRORS))

TARGET_COLUMNS = {
    "mass": "M",
    "radius": "R",
}

TARGET_ERROR_COLUMNS = {
    "mass": "eM",
    "radius": "eR",
}

# Use all three input features for the heteroscedastic GP variance model.
GP_VARIANCE_FEATURES = FEATURES

GP_MASS_TRACE_PATH = "Dataset_A_training/GP_mass_3features_allvar_1000_draws_80_40.nc"
HBNN_MASS_TRACE_PATH = "Dataset_A_training/HBNN_mass_3features_1000_draws_15_nodes_sig_015.nc"
BHS_MASS_PRED_PATH = f"{PREDICTION_OUTPUT_DIR}/BHS_mass_3features_holdout_predictions.csv"
BHS_MASS_WEIGHTS_PATH = f"{PREDICTION_OUTPUT_DIR}/BHS_mass_3features_holdout_weights.csv"

# Fallback normalization values. return_train_test/return_norm update these
# dictionaries from the selected training file before model training,
# prediction, or metric denormalization.
MU = {
    "Teff": 6185.617021276596,
    "Meta": -0.0460354609929078,
    "rho": 0.08959556919387729,
    "mass": 1.2379921985815603,
    "radius": 1.6715751773049645,
    #"logg": 4.103562701135996,
}

SIGMA = {
    "Teff": 433.7879065741058,
    "Meta": 0.20106141792491908,
    "rho": 0.07286057327576753,
    "mass": 0.20454705426768446,
    "radius": 0.44391533495523683,
    #"logg": 0.18650295415291138,
}
