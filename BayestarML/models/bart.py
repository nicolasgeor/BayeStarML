#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:27:50 2025

@author: LamirelFamily
"""


import operator

import numpy as np
import pymc as pm
import pymc_bart as pmb
from numba import njit

#######################################################################################
# How the input errors enter BART (checked 2026-11-15 on pymc_bart 0.11.0).
#
# The builders below give BART the inputs as X_dist ~ Normal(X, X_er). This is NOT an
# errors-in-variables model with latent inputs, unlike the HBNN:
#   - the tree sampler (PGBART) evaluates X_dist ONCE, when it is created, and trains every
#     tree on that single draw: the measured inputs plus one random realisation of their
#     errors (a noisy copy of the training inputs);
#   - nothing in the model links X_dist to the data (the BART term adds zero to the
#     log-probability), so the "latent" inputs are never inferred: their posterior is their prior;
#   - the input errors are propagated only when predicting: each predictive draw evaluates the
#     trees at a new draw of Normal(X_new, X_er_new).
#
# Decision (Nicolás, 2026-11-16): keep it as it is, and describe it this way in the paper
# (trees trained on one error-perturbed copy of the inputs, input errors propagated in the
# predictions), not as latent inputs.
#
# Since the same date the noisy copy and the trees are reproducible from the seed:
# see SeededPGBART and seed_bart_inputs at the end of this file.
#######################################################################################

def BART_M(X, X_er, Y, Y_er, m=250):
    """
    Build a BART model for predicting Y with input uncertainty in X.

    Constructs a PyMC model using Bayesian Additive Regression Trees (BART),
    where each input variable is treated as a normal random variable with
    mean `X` and standard deviation `X_er`. The model infers both the mean
    function and an uncertainty parameter for the target.

    Parameters
    ----------
    X : array-like
        Input features.
    X_er : array-like
        Measurement errors for each input feature.
    Y : array-like
        Observed target values.
    Y_er : array-like
        Measurement errors for Y (not used directly in the model).
    m : int, optional
        Number of trees in the BART ensemble. Default is 250.

    Returns
    -------
    pm.Model
        PyMC model defining the BART regression with learned noise parameter.
    """
    
    with pm.Model() as model_BART:
        
        X_in = pm.Data('X', X)
        X_in_er = pm.Data('X_er', X_er)
        
        X_normal = pm.Normal('X_dist', mu=X_in, sigma=X_in_er, shape=X_in.shape)
        
        mu = pmb.BART('mu', X_normal, Y.values, m=m)
             
        sig = pm.HalfCauchy('sig', beta=0.05)  # Difference with BART_R: here we infer the noise parameter instead of fixing it.
        # What we do here is defining a weakly informative prior to learn the standard deviation (noise) of the output from the data.
        
        y = pm.Normal("y", mu=mu, sigma=sig, shape=X_in.shape[0], observed=Y) # Defining the likelihood function.
        
    return model_BART


def BART_R(X, X_er, Y, Y_er, m=250):
    """
    Build a BART model with fixed output noise for predicting Y with input uncertainty.

    Similar to `BART_M`, but uses a fixed standard deviation (0.3) for the
    output noise instead of inferring it from the data.

    Parameters
    ----------
    X : array-like
        Input features.
    X_er : array-like
        Measurement errors for each input feature.
    Y : array-like
        Observed target values.
    Y_er : array-like
        Measurement errors for Y (not used directly in the model).
    m : int, optional
        Number of trees in the BART ensemble. Default is 250.

    Returns
    -------
    pm.Model
        PyMC model defining the BART regression with fixed noise parameter.
    """
    
    with pm.Model() as model_BART:
        
        X_in = pm.Data('X', X)
        X_in_er = pm.Data('X_er', X_er)
        
        X_normal = pm.Normal('X_dist', mu=X_in, sigma=X_in_er, shape=X_in.shape)
        
        mu = pmb.BART('mu', X_normal, Y.values, m=m)

        sig = 0.3

        y = pm.Normal("y", mu=mu, sigma=sig, shape=X_in.shape[0], observed=Y)

    return model_BART


def BART_floor(X, X_er, Y, Y_er, m=250):
    """
    Build a BART model whose output noise cannot fall below the measurement error of Y.

    Same as `BART_M`, but the noise of star i is sqrt(sig² + Y_er_i²): `sig` is inferred
    and is the scatter beyond the measurement error of the target. Used for both mass and
    radius when NOISE_MODEL = "floor" in run_pipeline.py.

    Parameters
    ----------
    X : array-like
        Input features.
    X_er : array-like
        Measurement errors for each input feature.
    Y : array-like
        Observed target values.
    Y_er : array-like
        Measurement errors for Y, in the same (normalised) units as Y.
    m : int, optional
        Number of trees in the BART ensemble. Default is 250.

    Returns
    -------
    pm.Model
        PyMC model defining the BART regression with a measurement-error noise floor.
    """

    with pm.Model() as model_BART:

        X_in = pm.Data('X', X)
        X_in_er = pm.Data('X_er', X_er)
        # A data container, so that it can be set to zero for the stars to predict
        # (see pred_sampling.sample_pred_BART): their draws then carry `sig` only.
        Y_in_er = pm.Data('Y_er', Y_er)

        X_normal = pm.Normal('X_dist', mu=X_in, sigma=X_in_er, shape=X_in.shape)

        mu = pmb.BART('mu', X_normal, Y.values, m=m)

        sig = pm.HalfCauchy('sig', beta=0.05)

        y = pm.Normal("y", mu=mu, sigma=pm.math.sqrt(sig**2 + Y_in_er**2), shape=X_in.shape[0], observed=Y)

    return model_BART



#######################################################################################
# Reproducible BART.
#
# pymc_bart 0.11.0 does not use the `random_seed` given to pm.sample for the trees: PGBART
# takes its random numbers from NumPy's global generator and from numba's own generator,
# and each chain runs in a new process where both start from an arbitrary state. The copy
# of the inputs the trees are trained on (see the top of this file) is drawn from yet
# another unseeded generator. Two runs with the same seed therefore gave different BARTs
# (e.g. radius, seed 665: LOO score 152.1 and 144.9).
#
# The three pieces below tie all of it to the seed. They rely on names inside pymc_bart
# (PGBART.normal, PGBART.uniform, PGBART.bart, the op's all_trees), so check them again
# if pymc_bart is upgraded.
#######################################################################################

@njit
def _seed_numba(seed):
    np.random.seed(seed)   # inside compiled code this seeds numba's generator, not NumPy's


def seed_bart_inputs(model, seed):
    """
    Seed everything PGBART uses when it is created in the main process: the generator behind
    X_dist (the noisy copy of the inputs is one draw from it) and the two global generators.
    Call it right before creating SeededPGBART.
    """
    node = model['X_dist'].owner
    node.op.rng_param(node).set_value(np.random.default_rng(seed), borrow=True)
    np.random.seed(seed)
    _seed_numba(seed)


class SeededPGBART(pmb.PGBART):
    """
    PGBART whose random numbers follow the seed PyMC gives to each chain.

    PyMC calls set_rng once per chain, inside the process that runs the chain, with a generator
    derived from `random_seed`. PGBART ignores it; here it seeds the two generators PGBART does use.

    The trees of every kept draw go to one list shared by all chains, in the order in which the
    processes happen to deliver them, and predictions pick trees from that list by position.
    So each entry is stored with (chain key, draw number) and order_bart_trees sorts the list
    after sampling: the predictions are then reproducible too.
    """

    _chain_key = 0
    _kept = 0

    def set_rng(self, rng):
        super().set_rng(rng)
        seed = int(self.rng.integers(2 ** 31 - 1))
        np.random.seed(seed)
        _seed_numba(seed)
        # Random numbers cached when the step was created, before the chain had its seed
        self.normal.update()
        self.uniform.update()
        self._chain_key = seed
        self._kept = 0

    def astep(self, _):
        shared = self.bart.all_trees
        kept = []
        self.bart.all_trees = kept      # PGBART appends the trees of a kept draw to this
        try:
            out = super().astep(_)
        finally:
            self.bart.all_trees = shared
        if kept:
            shared.append((self._chain_key, self._kept, kept[0]))
            self._kept += 1
        return out


class _OrderedTrees:
    """The shared list of (chain key, draw number, trees), read as a plain list of trees."""

    def __init__(self, stored):
        self._stored = stored

    def __len__(self):
        return len(self._stored)

    def __getitem__(self, index):
        return self._stored[int(index)][2]


def order_bart_trees(model, name='mu'):
    """
    Put the trees sampled with SeededPGBART in a fixed order (by chain key, then draw number).
    Call it after pm.sample and before sampling predictions. The sort runs inside the process
    that holds the list, so the trees are not copied.
    """
    op_class = type(model[name].owner.op)
    stored = op_class.all_trees
    stored.sort(key=operator.itemgetter(0, 1))
    op_class.all_trees = _OrderedTrees(stored)
