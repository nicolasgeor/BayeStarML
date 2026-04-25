#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 10:50:13 2025

@author: LamirelFamily
"""

from preprocess import return_train_test, prepare_pred4, denormalise_val, prepare_pred3
from utils import get_dataset, train, mard, mrd
from models import hbnn, bart, gp
from pred_sampling import sample_post_pred_HBNN_para, posterior_predictive_GP
import arviz as az
import numpy as np
import pymc as pm
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

df_train = get_dataset('Datasets/data_sample_calculated_density.txt', 'MS')
(x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
  mass_test, emass_test
) = return_train_test(df_train)

unorm_mass = denormalise_val(mass_test, 'mass')

x_train = x_train[['Teff', 'Meta', 'rho']]
x_train_er = x_train_er[['eTeff', 'eMeta', 'erho']]

x_test = x_test[['Teff', 'Meta', 'rho']]
x_test_er = x_test_err[['eTeff', 'eMeta', 'erho']]

# print(x_test3_er)

def main():
 
    # model = hbnn.HBNN_M4(x_train, rad_train, x_train_er, erad_train, 15)
    # model = hbnn.HBNN_M3(x_train, mass_train, x_train_er, emass_train, 15)

    model, μ_gp, log_var_gp, Xu, Xu_er = gp.sparse_fully_heteroscedastic_gp(x_train,
                                                                        x_train_er,
                                                                        mass_train, 80, 40)
    # Train is imported from another file, and runs MCMC sampling using PyMC.

    # trace = az.from_netcdf("Radius_output/HBNN_sig_015_15_nodes_mass_4_param.nc")
    
    # trace = train(model, "Radius_output/HBNN_sig_015_15_nodes_mass_4_param.nc", draw=1000, chains=2)

    # trace = az.from_netcdf("Radius_output/GP_hetero_new_2026_mass_4param_gamma_etav_80_40.nc")

    trace = train(model, "Train_outputs/GP_mass_3param_1000_draws_80_40.nc", draw=1000, chains=2)
    
    # trace = train(model, "Train_outputs/HBNN_mass_3param_1000_draws_15_nodes_sig_015.nc", draw=1000, chains=2)
        
    # trace.extend(pm.compute_log_likelihood(trace, model=model, var_names='y'))
    
    r_hat_values = az.rhat(trace)
    all_rhats = []
    for var in r_hat_values.data_vars:
        max_rhat = r_hat_values[var].max().values.item()
        all_rhats.append((var, max_rhat))

    print(all_rhats)
    
    print(az.loo(trace))
    
    pred, lpd = posterior_predictive_GP(
        model, μ_gp, log_var_gp, trace,
        x_test, x_test_er, Xu, Xu_er, 3, 'mass'
    )

    # pred, lpd = sample_post_pred_HBNN_para(
    #     trace, x_test, x_test_er, 15, 3, 'mass'
    # )

    # pred, lpd = sample_post_pred_HBNN_para(trace, x_test, x_test_er, 15, 4, 'mass')

    print(pred.std(0))
    print(pred.mean(0))
    print(unorm_mass)
    
    print('MAE: ', mean_absolute_error(unorm_mass, pred.mean(0)))
    
    print('MARD', mard(unorm_mass, pred.mean(0)))
    
    print('MRD', mrd(unorm_mass, pred.mean(0)))

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass, pred.mean(0), yerr=pred.std(0), fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.plot([unorm_mass.min(), unorm_mass.max()], [unorm_mass.min(), unorm_mass.max()], 'r--')
    plt.xlabel('True Mass')
    plt.ylabel('Predicted Mass')
    plt.title('HBNN Predictions with Uncertainty')
    plt.legend()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.errorbar(unorm_mass, pred.mean(0) - unorm_mass, yerr=pred.std(0), fmt='o', label='Predictions with Uncertainty', alpha=0.7)
    plt.hlines(0, unorm_mass.min(), unorm_mass.max(), 'r', linestyle='--')
    plt.xlabel('True Mass')
    plt.ylabel('Residual Mass')
    # plt.title('HBNN Predictions with Uncertainty')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()