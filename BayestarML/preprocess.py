#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 18:03:17 2025

@author: LamirelFamily
"""

"""Utility functions shared by many modules."""

import numpy as np
import pandas as pd
from constants import MU, SIGMA
from utils import get_dataset
from sklearn.model_selection import train_test_split

RANDOM_SEED = 4159 # Default train/test split seed; run_pipeline.py passes its own SPLIT_SEED

# Column and error column for each prediction target
TARGET_COLUMNS = {'radius': ('R', 'eR'), 'mass': ('M', 'eM')}


def normalise_val(x: float | None, key: str) -> float:
    return np.nan if x is None else (x - MU[key]) / SIGMA[key]


def normalise_err(e: float | None, key: str) -> float:
    return np.nan if e is None else abs(e) / SIGMA[key]


def denormalise_val(y: np.ndarray, key: str) -> np.ndarray:
    return y * SIGMA[key] + MU[key]

def denormalise_err(y: np.ndarray, key: str) -> np.ndarray:
    return y * SIGMA[key]


def return_norm(df, random_state=RANDOM_SEED):
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
        Input DataFrame containing stellar parameters (`Teff`, `logg`, `Meta`, `L`, `M`)
        and their asymmetric uncertainties (`eX1`, `eX2` for lower/upper errors).
    random_state : int
        Seed for the train/test split. Must match the one used for training.

    Returns
    -------
    tuple
        (mteff, mlogg, mmet, mlum, mtmass, steff, slogg, smet, slum, smass)
        Mean and standard deviation for each variable, in the order:
        effective temperature, surface gravity, metallicity, luminosity, and mass.
    """
    df1 = df[['eTeff1', 'elogg1', 'eMeta1', 'eL1', 'eM1', 'eR1']].copy()
    df2 = df[['eTeff2', 'elogg2', 'eMeta2', 'eL2', 'eM2', 'eR2']].copy()
    df2.columns = ['eTeff1', 'elogg1', 'eMeta1', 'eL1', 'eM1', 'eR1']

    # Mean error if non-symetric

    X_error = (df1 + df2) / 2 
    X_error.columns = ['eTeff', 'elogg', 'eMeta', 'eL', 'eM', 'eR']

    X = pd.concat([df[['Teff', 'logg', 'Meta', 'L']],
                   X_error[['eTeff', 'elogg', 'eMeta', 'eL']]],
                  axis=1)
    
    # Y = pd.concat([df['M'], X_error['eM']], axis=1)
    Y = pd.concat([df['R'], X_error['eR']], axis=1)
    
    # do split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                        test_size=154,
                                                        random_state=random_state)

    # Extract relevant columns for stellar mass prediction
    teff = X_train['Teff']
    logg = X_train['logg']
    met = X_train['Meta']
    lum = X_train['L']
    # mass = Y_train["M"]    
    rad = Y_train['R']


    # Compute means and standard deviations for standardization
    mteff = np.mean(teff)
    mlogg = np.mean(logg)
    mmet = np.mean(met)
    mlum = np.mean(lum)
    # mtmass = np.mean(mass)
    mtrad = np.mean(rad)

    steff = np.std(teff)
    slogg = np.std(logg)
    smet = np.std(met)
    slum = np.std(lum)
    # smass = np.std(mass)
    srad = np.std(rad)

    # return mteff, mlogg, mmet, mlum, mtmass, steff, slogg, smet, slum, smass     
    return mteff, mlogg, mmet, mlum, mtrad, steff, slogg, smet, slum, srad     

def return_train_test(df, normalised=True, target='radius', random_state=RANDOM_SEED):
    """

    Parameters
    ----------
    df : TYPE, pandas df
        DESCRIPTION. The default is df. All data.
    normalised : TYPE, bool
        DESCRIPTION. The default is True.
    target : str, 'radius' or 'mass'
        Which quantity is returned (normalised) as the target y. The default is 'radius'.
    random_state : int
        Seed for the train/test split. The default is RANDOM_SEED.

    Returns
    -------
    normalised or not normalised training and testing data. 
    Note that normalised and non normalised don't come in the same format
    For normalised: x_train, x_train_er, x_test, x_test_error,
    y, ey, y_test, ey_test (y is the radius or the mass, depending on `target`)
    For non normalised: X_train, X_test, Y_train, Y_test / where errors and
    data are combined
    
    if you want both just call twice

    """
    y_col, ey_col = TARGET_COLUMNS[target]

    df1 = df[['eTeff1', 'elogg1', 'eMeta1', 'eL1', 'eM1', 'eR1']].copy()
    df2 = df[['eTeff2', 'elogg2', 'eMeta2', 'eL2', 'eM2', 'eR2']].copy()
    df2.columns = ['eTeff1', 'elogg1', 'eMeta1', 'eL1', 'eM1', 'eR1']

    # Mean error if non-symmetric
    X_error = (df1 + df2) / 2 


    X_error.columns = ['eTeff', 'elogg', 'eMeta', 'eL', 'eM', 'eR']  

    X = pd.concat([df[['Teff', 'logg', 'Meta', 'L']],
                    X_error[['eTeff', 'elogg', 'eMeta', 'eL']]],
                    axis=1)
    Y = pd.concat([df['M'], X_error['eM'], df['R'], X_error['eR']], axis=1)
    
    # do split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                        test_size=154,
                                                        random_state=random_state)

    # Extract relevant columns for stellar mass or radius prediction
    teff = X_train['Teff']
    logg = X_train['logg']
    met = X_train['Meta']
    lum = X_train['L']
    y = Y_train[y_col]

    # Compute means and standard deviations for standardization (training split only)
    mteff = np.mean(teff)
    mlogg = np.mean(logg)
    mmet = np.mean(met)
    mlum = np.mean(lum)
    my = np.mean(y)

    steff = np.std(teff)
    slogg = np.std(logg)
    smet = np.std(met)
    slum = np.std(lum)
    sy = np.std(y)

    # Standardize inputs 
    teff = (teff - mteff) / steff
    logg = (logg - mlogg) / slogg
    met = (met - mmet) / smet
    lum = (lum - mlum) / slum
    y = (y - my) / sy

    # Uncertainties for the inputs
    eteff = X_train['eTeff'] / steff
    elogg = X_train['elogg'] / slogg
    emet = abs(X_train['eMeta']) / smet
    elum = X_train['eL'] / slum  
    ey = Y_train[ey_col] / sy


    x_train = pd.concat([teff, logg, met, lum], axis=1)
    x_train_er = pd.concat([eteff, elogg, emet, elum], axis=1)

    teff_test = (X_test['Teff'] - mteff) / steff
    logg_test = (X_test['logg'] - mlogg) / slogg
    met_test = (X_test['Meta'] - mmet) / smet
    lum_test = (X_test['L'] - mlum) / slum
    y_test = (Y_test[y_col] - my) / sy

    x_test = pd.concat([teff_test, logg_test, met_test, lum_test], axis=1)

    eteff_test = X_test['eTeff'] / steff
    elogg_test = X_test['elogg'] / slogg
    emet_test = abs(X_test['eMeta']) / smet
    elum_test = X_test['eL'] / slum 
    ey_test = Y_test[ey_col] / sy

    x_test_error = pd.concat([eteff_test, elogg_test, emet_test, elum_test], axis=1)
    
    if normalised == True:
        return x_train, x_train_er, x_test, x_test_error, y, ey, y_test, ey_test
    
    if normalised == False:
        return X_train, X_test, Y_train, Y_test
    
def prepare_pred4(filename):
    """
    Normalize input data and return DataFrames for normalized values and errors.
    
    Parameters:
    - teff, logg, meta, l: Input values (can be scalars or arrays)
    - eteff, elogg, emeta, el: Associated errors (can be scalars or arrays)
    - codeword: Value that indicates missing data (will be converted to NaN)
    
    Returns:
    - x_test: DataFrame with normalized values (columns: 'Teff', 'logg', 'Meta', 'L')
    - x_test_error: DataFrame with normalized errors (columns: 'eTeff', 'elogg', 'eMeta', 'eL')
    """
    
    X = pd.read_csv(filename)
    df = get_dataset('Datasets/database_D_old_format.txt', 'MS')
    df = df[df['mode'] == 'A']
    # mteff, mlogg, mmet, mlum, mtmass, steff, slogg, smet, slum, smass = return_norm(df)
    mteff, mlogg, mmet, mlum, mtrad, steff, slogg, smet, slum, srad = return_norm(df)

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
        'Teff': normalize(X['Teff'], mteff, steff),
        'logg': normalize(X['logg'], mlogg, slogg),
        'Meta': normalize(X['Meta'], mmet, smet),
        'L': normalize(X['L'], mlum, slum)
    }
    
    error_data = {
        'eTeff': normalize_error(X['eTeff'], steff),
        'elogg': normalize_error(X['elogg'], slogg),
        'eMeta': normalize_error(X['eMeta'], smet),
        'eL': normalize_error(X['eL'], slum)
    }
    

    # For scalar inputs, we need to create a single-row DataFrame
    if (not hasattr(X['Teff'], '__len__') or isinstance(X['Teff'], str)) and X['Teff'] is not None:
        x_test = pd.DataFrame(norm_data, index=[0])
        x_test_error = pd.DataFrame(error_data, index=[0])
    else:
        x_test = pd.DataFrame(norm_data)
        x_test_error = pd.DataFrame(error_data)
    
    return x_test, x_test_error

def prepare_pred3(filename):
    """
    Normalize input data and return DataFrames for normalized values and errors.
    
    Parameters:
    - teff, logg, meta, l: Input values (can be scalars or arrays)
    - eteff, elogg, emeta, el: Associated errors (can be scalars or arrays)
    - codeword: Value that indicates missing data (will be converted to NaN)
    
    Returns:
    - x_test: DataFrame with normalized values (columns: 'Teff', 'logg', 'Meta', 'L')
    - x_test_error: DataFrame with normalized errors (columns: 'eTeff', 'elogg', 'eMeta', 'eL')
    """
    
    X = pd.read_csv(filename)
    df = get_dataset('Datasets/database_A_old_format_with_xiong_log_L.txt', 'MS')
    # mteff, mlogg, mmet, mlum, mtmass, steff, slogg, smet, slum, smass = return_norm(df)
    mteff, mlogg, mmet, mlum, mtrad, steff, slogg, smet, slum, srad = return_norm(df)

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
        'Teff': normalize(X['Teff'], mteff, steff),
        'Meta': normalize(X['Meta'], mmet, smet),
        'L': normalize(X['L'], mlum, slum)
    }
    
    error_data = {
        'eTeff': normalize_error(X['eTeff'], steff),
        'eMeta': normalize_error(X['eMeta'], smet),
        'eL': normalize_error(X['eL'], slum)
    }
    
    if (not hasattr(X['Teff'], '__len__') or isinstance(X['Teff'], str)) and X['Teff'] is not None:
        x_test = pd.DataFrame(norm_data, index=[0])
        x_test_error = pd.DataFrame(error_data, index=[0])
    else:
        x_test = pd.DataFrame(norm_data)
        x_test_error = pd.DataFrame(error_data)
    
    return x_test, x_test_error

