#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 17:55:32 2025

@author: LamirelFamily
"""

TARGET = "mass"

DATASET_PATH = "Datasets/database_A_old_format.txt"

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

GP_MASS_TRACE_PATH = "Train_outputs/GP_mass_3features_allvar_1000_draws_80_40.nc"
HBNN_MASS_TRACE_PATH = "Train_outputs/HBNN_mass_3param_1000_draws_15_nodes_sig_015.nc"

# These values match the current training split produced from DATASET_PATH
# with RANDOM_SEED = 5732.
# If the dataset or split changes, regenerate these values before trusting
# physical-scale predictions or metrics.
MU = {
    "Teff": 6100.907928802589,
    "Meta": -0.06768802588996764,
    "rho": 0.7145431877022653,
    "mass": 1.1987114886731391,
    "radius": 1.5685433656957928,
    #"logg": 4.103562701135996,
}

SIGMA = {
    "Teff": 806.8961103261462,
    "Meta": 0.209019330842107,
    "rho": 1.5938993081018857,
    "mass": 0.30516492476714924,
    "radius": 0.5522783155512756,
    #"logg": 0.18650295415291138,
}
