#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 18:03:17 2025

@author: LamirelFamily
"""

"""Utility functions shared by many modules."""

import numpy as np
import pandas as pd
from constants import (
    FEATURE_ERRORS,
    FEATURES,
    MU,
    SIGMA,
    TARGET,
    TARGET_COLUMNS,
    TARGET_ERROR_COLUMNS,
    TRAINING_DATA_FILE,
)
from utils import get_dataset, load_stellar_dataframe
from sklearn.model_selection import train_test_split

RANDOM_SEED = 5732 


RAW_ERROR_COLUMNS = {
    "eTeff": ("eTeff1", "eTeff2"),
    "eMeta": ("eMeta1", "eMeta2"),
    "erho": ("erho1", "erho2"),
    "eM": ("eM1", "eM2"),
    "eR": ("eR1", "eR2"),
}


def _check_target(target: str) -> None:
    if target != TARGET:
        raise NotImplementedError(
            f"This 3-feature workflow is configured for target={TARGET!r}. "
            f"Got target={target!r}."
        )


def _mean_symmetric_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Average the two reported uncertainty columns into one error column."""
    errors = {}
    for out_col, (lo_col, hi_col) in RAW_ERROR_COLUMNS.items():
        sides = df[[lo_col, hi_col]].abs()
        sides = sides.where(sides > 0)
        errors[out_col] = sides.mean(axis=1, skipna=True)
    return pd.DataFrame(errors, index=df.index)


def _set_normalisation_stats(mteff, mmet, mrho, mtmass, steff, smet, srho, smass, target):
    MU.update({
        FEATURES[0]: mteff,
        FEATURES[1]: mmet,
        FEATURES[2]: mrho,
        target: mtmass,
    })
    SIGMA.update({
        FEATURES[0]: steff,
        FEATURES[1]: smet,
        FEATURES[2]: srho,
        target: smass,
    })


def normalise_val(x: float | None, key: str) -> float:
    return np.nan if x is None else (x - MU[key]) / SIGMA[key]


def normalise_err(e: float | None, key: str) -> float:
    return np.nan if e is None else abs(e) / SIGMA[key]


def denormalise_val(y: np.ndarray, key: str) -> np.ndarray:
    return y * SIGMA[key] + MU[key]

def denormalise_err(y: np.ndarray, key: str) -> np.ndarray:
    return y * SIGMA[key]


def return_norm(df, target: str = TARGET):
    """
    Compute normalization statistics for stellar parameters and their errors.

    Extracts stellar feature (feature=input variable) columns and their associated asymmetric measurement
    uncertainties, computes symmetric mean errors, splits the dataset into
    training and test sets, and calculates the mean and standard deviation
    of each input and target variable for normalization.
    
    We normalize because if we just feed a neural network a Temperature of 5500 and a Metallicity of -0.5, 
    the massive difference in scale will cause the math to completely break down.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing the configured 3 input features
        (`Teff`, `Meta`, `rho`), the mass target, and asymmetric uncertainties.

    Returns
    -------
    tuple
        Mean and standard deviation for each variable, in the order:
        effective temperature, metallicity, density, and mass.
    """
    _check_target(target)
    target_column = TARGET_COLUMNS[target]
    target_error_column = TARGET_ERROR_COLUMNS[target]

    X_error = _mean_symmetric_errors(df)

    X = pd.concat([df[FEATURES],
                   X_error[FEATURE_ERRORS]],
                  axis=1)
    
    Y = pd.concat([df[target_column], X_error[target_error_column]], axis=1)
    
    # do split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                        test_size=0.2,
                                                        random_state=RANDOM_SEED)

    teff = X_train[FEATURES[0]]
    met = X_train[FEATURES[1]]
    rho = X_train[FEATURES[2]]
    target_values = Y_train[target_column]


    # Compute means and standard deviations for standardization
    mteff = np.mean(teff)
    mmet = np.mean(met)
    mrho = np.mean(rho)
    mtmass = np.mean(target_values)

    steff = np.std(teff)
    smet = np.std(met)
    srho = np.std(rho)
    smass = np.std(target_values)
    _set_normalisation_stats(mteff, mmet, mrho, mtmass, steff, smet, srho, smass, target)
    
    return mteff, mmet, mrho, mtmass, steff, smet, srho, smass     

def return_train_test(df, normalised=True, target: str = TARGET):
    """

    Parameters
    ----------
    df : TYPE, pandas df
        DESCRIPTION. The default is df. All data.
    normalised : TYPE, bool
        DESCRIPTION. The default is True.

    Returns
    -------
    normalised or not normalised training and testing data. 
    Note that normalised and non normalised don't come in the same format
    For normalised: x_train, x_train_er, x_test, x_test_error,
    y_train, y_train_error, y_test, y_test_error
    For non normalised: X_train, X_test, Y_train, Y_test / where errors and
    data are combined
    
    if you want both just call twice

    """
    _check_target(target)
    target_column = TARGET_COLUMNS[target]
    target_error_column = TARGET_ERROR_COLUMNS[target]

    X_error = _mean_symmetric_errors(df)

    X = pd.concat([df[FEATURES],
                   X_error[FEATURE_ERRORS]],
                  axis=1)
    Y = pd.concat([df[target_column], X_error[target_error_column]], axis=1)
    
    # do split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                        test_size=0.2,
                                                        random_state=RANDOM_SEED)

    teff = X_train[FEATURES[0]]
    met = X_train[FEATURES[1]]
    rho = X_train[FEATURES[2]]
    y_train = Y_train[target_column]

    # Compute means and standard deviations for standardization
    mteff = np.mean(teff)
    mmet = np.mean(met)
    mrho = np.mean(rho)
    mtmass = np.mean(y_train)
    
    steff = np.std(teff)
    smet = np.std(met)
    srho = np.std(rho)
    smass = np.std(y_train)
    _set_normalisation_stats(mteff, mmet, mrho, mtmass, steff, smet, srho, smass, target)
    
    # Standardize inputs 
    teff = (teff - mteff) / steff
    met = (met - mmet) / smet
    rho = (rho - mrho) / srho
    y_train = (y_train - mtmass) / smass


    # Uncertainties for the inputs
    eteff = X_train['eTeff'] / steff
    emet = abs(X_train['eMeta']) / smet
    erho = X_train['erho'] / srho  
    y_train_error = Y_train[target_error_column] / smass

    x_train = pd.concat([teff, met, rho], axis=1)
    x_train.columns = FEATURES
    x_train_er = pd.concat([eteff, emet, erho], axis=1)
    x_train_er.columns = FEATURE_ERRORS

    teff_test = (X_test[FEATURES[0]] - mteff) / steff
    met_test = (X_test[FEATURES[1]] - mmet) / smet
    rho_test = (X_test[FEATURES[2]] - mrho) / srho
    y_test = (Y_test[target_column] - mtmass) / smass

    x_test = pd.concat([teff_test, met_test, rho_test], axis=1)
    x_test.columns = FEATURES

    eteff_test = X_test['eTeff'] / steff
    emet_test = abs(X_test['eMeta']) / smet
    erho_test = X_test['erho'] / srho 
    y_test_error = Y_test[target_error_column] / smass

    x_test_error = pd.concat([eteff_test, emet_test, erho_test], axis=1)
    x_test_error.columns = FEATURE_ERRORS

    
    if normalised == True:
        return (
            x_train, x_train_er,
            x_test, x_test_error,
            y_train, y_train_error,
            y_test, y_test_error,
        )
    
    if normalised == False:
        return X_train, X_test, Y_train, Y_test
    
def prepare_pred4(filename):
    """
    The 4-feature model path is intentionally disabled for the current thesis
    workflow. Use prepare_pred3 for Teff, Meta, and rho.
    """
    raise NotImplementedError(
        "The active thesis workflow is the 3-feature Mass model: "
        "Teff, Meta, and rho. Use prepare_pred3 instead."
    )

def prepare_pred3(filename, target: str = TARGET):
    """
    Normalize input data and return DataFrames for normalized values and errors.
    
    Input CSV must contain columns: Teff, Meta, rho, eTeff, eMeta, erho.

    Returns:
    - x_test: DataFrame with normalized values (columns: Teff, Meta, rho)
    - x_test_error: DataFrame with normalized errors (columns: eTeff, eMeta, erho)
    """
    
    _check_target(target)
    X, _ = load_stellar_dataframe(
        filename,
        required_features=FEATURES,
        target=target,
        star_class=None,
        drop_invalid=True,
    )
    df = get_dataset(TRAINING_DATA_FILE, 'MS', features=FEATURES, target=target)
    mteff, mmet, mrho, mtmass, steff, smet, srho, smass = return_norm(df, target=target)

    # Helper function to normalize and handle missing values
    def normalize(value, mean, std):
        if value is None:
            return np.nan
        return (np.array(value) - mean) / std
    
    # Helper function to normalize errors (absolute value)
    def normalize_error(error, std):
        if error is None:
            return np.nan
        return abs(np.array(error)) / std
    
    # Normalize each parameter and its error
    norm_data = {
        FEATURES[0]: normalize(X[FEATURES[0]], mteff, steff),
        FEATURES[1]: normalize(X[FEATURES[1]], mmet, smet),
        FEATURES[2]: normalize(X[FEATURES[2]], mrho, srho)
    }
    
    error_data = {
        FEATURE_ERRORS[0]: normalize_error(X[FEATURE_ERRORS[0]], steff),
        FEATURE_ERRORS[1]: normalize_error(X[FEATURE_ERRORS[1]], smet),
        FEATURE_ERRORS[2]: normalize_error(X[FEATURE_ERRORS[2]], srho)
    }
    
    if (
        (not hasattr(X[FEATURES[0]], "__len__") or isinstance(X[FEATURES[0]], str))
        and X[FEATURES[0]] is not None
    ):
        x_test = pd.DataFrame(norm_data, index=[0])
        x_test_error = pd.DataFrame(error_data, index=[0])
    else:
        x_test = pd.DataFrame(norm_data)
        x_test_error = pd.DataFrame(error_data)
    
    return x_test, x_test_error

