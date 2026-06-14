#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:45:46 2025

@author: LamirelFamily
"""

import arviz as az
import pandas as pd
import numpy as np
import pymc as pm

def get_dataset(data_file, star_class, filter_mode='luminosity'):
    """
    Load and clean a stellar dataset for a given star class.

    Reads a tab-separated file of stellar parameters and their uncertainties,
    filters rows matching the specified class, removes entries with missing
    values for the requested feature set, and returns the cleaned subset.

    Parameters
    ----------
    data_file : str
        Path to the tab-separated data file.
    star_class : str
        Stellar class to filter by (e.g., 'MS').
    filter_mode : {'luminosity', 'rho'}, optional
        Feature set used to decide which rows are usable. ``'luminosity'``
        keeps the historical Teff/Meta/L filter. ``'rho'`` keeps stars with
        valid Teff/Meta/rho measurements and does not reject rows only because
        their luminosity uncertainty is unavailable or zero.

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame containing stars of the given class.
    """
    data = pd.read_table(data_file, sep="\t", comment="%")
    # read data with errors
    data_MS = data[data['class'] == star_class]
    # select Main Sequence Stars
    base_cols = ['Seq', 'R', 'eR1', 'eR2', 'M', 'eM1', 'eM2',
                 'Teff', 'eTeff1', 'eTeff2', 'Meta', 'eMeta1', 'eMeta2']
    uncertainty_cols = ['eR1', 'eR2', 'eM1', 'eM2',
                        'eTeff1', 'eTeff2', 'eMeta1', 'eMeta2']

    if filter_mode == 'luminosity':
        required_cols = base_cols + ['L', 'eL1', 'eL2']
        uncertainty_cols = uncertainty_cols + ['eL1', 'eL2']
    elif filter_mode == 'rho':
        required_cols = base_cols + ['rho', 'erho1', 'erho2']
        uncertainty_cols = uncertainty_cols + ['erho1', 'erho2']
    else:
        raise ValueError("filter_mode must be either 'luminosity' or 'rho'")

    missing_cols = [col for col in required_cols if col not in data_MS.columns]
    if missing_cols:
        raise ValueError(
            f"{data_file} is missing columns required for {filter_mode!r} "
            f"filtering: {missing_cols}"
        )

    df = data_MS[required_cols].copy()

    # clean NA values (simply remove the corresponding rows)
    df.dropna(inplace=True, axis=0)
    df = df[(df[uncertainty_cols] != 0).all(axis=1)]
    df_complete = data_MS.loc[df.index].copy()

    return df_complete
    

def find_pointwise_loo(trace):
    """
    Compute pointwise leave-one-out (LOO) log predictive densities.

    Parameters
    ----------
    trace : arviz.InferenceData
        Posterior trace containing log-likelihood values.

    Returns
    -------
    numpy.ndarray
        Array of pointwise LOO log-scores for each data point.
    """
    return az.loo(trace, pointwise=True, scale="log").loo_i.values


def train(model, filename, draw=1000, chains=2, target_accept=0.95, random_seed=225):
    """
    Sample from a PyMC model and save the posterior trace.

    Runs MCMC sampling, computes log-likelihoods, and stores the trace 
    in a NetCDF file.

    Parameters
    ----------
    model : pm.Model
        The PyMC model to sample from.
    filename : str
        Path to save the resulting trace file.
    draw : int, optional
        Number of posterior samples per chain. Default is 1000.
    chains : int, optional
        Number of MCMC chains. Default is 2.
    target_accept : float, optional
        Target acceptance rate for the sampler. Default is 0.95.


    Returns
    -------
    arviz.InferenceData
        Posterior samples with computed log-likelihoods.
    """
    print('target_accept=', target_accept)
    trace = pm.sample(draws=draw, tune=draw, chains=chains, model=model,
                      target_accept=target_accept, random_seed=random_seed)
    trace.extend(pm.compute_log_likelihood(trace, model=model, var_names='y'))
    trace.to_netcdf(filename)

    return trace


def mard(y_true, y_pred):
    """
    Compute the mean absolute relative difference (MARD) in percent.

    Parameters
    ----------
    y_true : array-like
        True target values.
    y_pred : array-like
        Predicted values.

    Returns
    -------
    float
        Mean absolute relative difference (percentage).
    """
    relative_diff = np.abs((np.array(y_true) - np.array(y_pred)) / np.array(y_true))
    return np.mean(relative_diff) * 100

def mrd(y_true, y_pred):
    """
    Compute the mean relative difference (MRD) in percent.

    Parameters
    ----------
    y_true : array-like
        True target values.
    y_pred : array-like
        Predicted values.

    Returns
    -------
    float
        Mean relative difference (percentage).
    """
    relative_diff = (np.array(y_true) - np.array(y_pred)) / np.array(y_true)
    return np.mean(relative_diff) * 100  
    
    
    
