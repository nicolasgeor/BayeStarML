#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 15:52:30 2025

@author: LamirelFamily
"""

from preprocess import return_train_test, prepare_pred4, denormalise_val, prepare_pred3
from utils import get_dataset, mard, mrd
from models import bart, gp
from pred_sampling import sample_pred_BART, posterior_predictive_GP, sample_post_pred_HBNN_para
from bhs import run_stack
import arviz as az
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.lines import Line2D
# import pymc as pm
# from sklearn.metrics import mean_absolute_error
# from utils import find_pointwise_loo

OUTPUT_DIR = r'C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_B_training_17_june'
TRAINING_FILE = 'Datasets/database_B.txt'
SAMPLING_SEED = 176
MASS_AXIS_LIMITS = (0.4, 2.0)
PLOT_BLUE = '#2563EB'
AXIS_LABEL_SIZE = 18
TICK_LABEL_SIZE = 14
LEGEND_SIZE = 15


def _legend_handle():
    return Line2D(
        [0], [0],
        marker='o',
        color=PLOT_BLUE,
        markerfacecolor='black',
        markeredgecolor='black',
        linestyle='-',
        linewidth=1.5,
    )


def _style_mass_axis(ax, ylabel):
    ax.set_xlim(*MASS_AXIS_LIMITS)
    ax.set_xlabel('True Mass', fontsize=AXIS_LABEL_SIZE)
    ax.set_ylabel(ylabel, fontsize=AXIS_LABEL_SIZE)
    ax.tick_params(axis='both', labelsize=TICK_LABEL_SIZE)
    ax.legend(
        [_legend_handle()],
        ['Predictions with Uncertainty'],
        fontsize=LEGEND_SIZE,
        loc='upper left',
        frameon=True,
    )


def _residual_spread(residual, pred_sigma):
    spread = np.nanmax(np.abs(residual) + pred_sigma)
    if not np.isfinite(spread):
        return 0.25
    return max(0.25, float(spread) * 1.1)

def plot_mass_diagnostics(unorm_mass, pred, model_name, filtered_percentiles=(95,), output_base=None):
    M_pred_sigma = pred.std(0)
    M_pred_mean = pred.mean(0)
    if output_base is not None:
        os.makedirs(os.path.dirname(output_base), exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(unorm_mass, M_pred_mean, yerr=M_pred_sigma, fmt='o',
                color='black', markerfacecolor='black', markeredgecolor='black',
                ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
    ax.plot(MASS_AXIS_LIMITS, MASS_AXIS_LIMITS, 'r--', linewidth=1.7)
    ax.set_ylim(*MASS_AXIS_LIMITS)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    ax.set_yticks(np.arange(0.4, 2.01, 0.2))
    _style_mass_axis(ax, 'Predicted Mass')
    if output_base is not None:
        fig.savefig(output_base + '_full_prediction.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close(fig)

    residual = M_pred_mean - unorm_mass
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(unorm_mass, residual, yerr=M_pred_sigma, fmt='o',
                color='black', markerfacecolor='black', markeredgecolor='black',
                ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
    ax.hlines(0, *MASS_AXIS_LIMITS, colors='red', linestyles='--', linewidth=1.7)
    ax.set_xticks(np.arange(0.4, 2.01, 0.2))
    ax.set_ylim(-_residual_spread(residual, M_pred_sigma), _residual_spread(residual, M_pred_sigma))
    _style_mass_axis(ax, 'Residual Mass')
    if output_base is not None:
        fig.savefig(output_base + '_full_residual.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close(fig)

    for percentile in filtered_percentiles:
        sigma_cut = np.percentile(M_pred_sigma, percentile)
        plot_mask = M_pred_sigma < sigma_cut
        unorm_mass_plot = np.asarray(unorm_mass)[plot_mask]
        M_pred_mean_plot = M_pred_mean[plot_mask]
        M_pred_sigma_plot = M_pred_sigma[plot_mask]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(unorm_mass_plot, M_pred_mean_plot, yerr=M_pred_sigma_plot, fmt='o',
                    color='black', markerfacecolor='black', markeredgecolor='black',
                    ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
        ax.plot(MASS_AXIS_LIMITS, MASS_AXIS_LIMITS, 'r--', linewidth=1.7)
        ax.set_ylim(*MASS_AXIS_LIMITS)
        ax.set_xticks(np.arange(0.4, 2.01, 0.2))
        ax.set_yticks(np.arange(0.4, 2.01, 0.2))
        _style_mass_axis(ax, 'Predicted Mass')
        if output_base is not None:
            fig.savefig(output_base + f'_filtered_{percentile}_prediction.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)

        residual_plot = M_pred_mean_plot - unorm_mass_plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(unorm_mass_plot, residual_plot, yerr=M_pred_sigma_plot, fmt='o',
                    color='black', markerfacecolor='black', markeredgecolor='black',
                    ecolor=PLOT_BLUE, elinewidth=1.5, alpha=0.75)
        ax.hlines(0, *MASS_AXIS_LIMITS, colors='red', linestyles='--', linewidth=1.7)
        ax.set_xticks(np.arange(0.4, 2.01, 0.2))
        ax.set_ylim(-_residual_spread(residual_plot, M_pred_sigma_plot), _residual_spread(residual_plot, M_pred_sigma_plot))
        _style_mass_axis(ax, 'Residual Mass')
        if output_base is not None:
            fig.savefig(output_base + f'_filtered_{percentile}_residual.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.close(fig)

# This prediction for 4 variables is very probably broken now
def predict4(X, X_er, target, test=False):
    
    df_train = get_dataset('Datasets/data_sample_calculated_density.txt', 'MS')
    (x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
    mass_test, emass_test
    ) = return_train_test(df_train)
    
    if test == True:
        X = x_test
        X_er = x_test_err

    if target == 'mass':
        
        unorm_mass = denormalise_val(mass_test, 'mass')
        
        
        bart4_model = bart.BART_M(x_train, x_train_er, mass_train, emass_train)
        bart4_pred, lpd_BART4 = sample_pred_BART(bart4_model,
                                      X,
                                      X_er, 'mass',
                                      1000, 2)


        gp4_model, μ_gp4, lg_σ_gp4, Xu4, Xu_er4 = gp.sparse_fully_heteroscedastic_gp(x_train, x_train_er, mass_train, 80, 40)

        # Loads the trace from the trained GP model (the learned weights and hyperparamenters)    
        gp4_trace = az.from_netcdf('models/model_artifacts/gp_mass_80_40.nc')
        gp4_pred, lpd_GP4 = posterior_predictive_GP(gp4_model, μ_gp4, lg_σ_gp4, 
                                            gp4_trace, X,
                                            X_er,
                                            Xu4, Xu_er4, 4, 'mass')

        
        # Loads the trace from the trained HBNN model (the learned weights and hyperparamenters)    
        hbnn4_trace = az.from_netcdf('models/model_artifacts/HBNN_mass.nc')
        hbnn4_pred, lpd_HBNN4 = sample_post_pred_HBNN_para(hbnn4_trace,  
                                                      X,
                                                      X_er,
                                                      15, 4, 'mass')


        (bhs_trace, bhs_pred, bhs_w) = run_stack(bart4_pred, hbnn4_pred, gp4_pred,
                                            x_train, X, lpd_BART4, lpd_HBNN4,
                                            lpd_GP4)

        if test == True:
            mard_BART = mard(unorm_mass, bart4_pred.mean(0))
            mrd_BART = mrd(unorm_mass, bart4_pred.mean(0))
            
            print('MARD BART:', mard_BART)
            print('MRD BART:', mrd_BART)
            
            mard_GP = mard(unorm_mass, gp4_pred.mean(0))
            mrd_GP = mrd(unorm_mass, gp4_pred.mean(0))
            
            print('MARD GP:', mard_GP)
            print('MRD GP:', mrd_GP)
            
            mard_HBNN = mard(unorm_mass, hbnn4_pred.mean(0))
            mrd_HBNN = mrd(unorm_mass, hbnn4_pred.mean(0))
            
            print('MARD HBNN:', mard_HBNN)
            print('MRD HBNN:', mrd_HBNN)
            
            mard_BHS = mard(unorm_mass, bhs_pred.mean(0))
            mrd_BHS = mrd(unorm_mass, bhs_pred.mean(0))
            
            print('MARD BHS:', mard_BHS)
            print('MRD BHS:', mrd_BHS)
            
        
        return [bart4_pred, gp4_pred, hbnn4_pred], bhs_pred, bhs_w
    
    if target == 'radius':
        
        unorm_rad = denormalise_val(rad_train, 'radius') # Check if this should be rad_test instead of rad_train
        
        
        bart4_model = bart.BART_R(x_train, x_train_er, rad_train, erad_train)
        bart4_pred, lpd_BART4 = sample_pred_BART(bart4_model,
                                      X,
                                      X_er, 'radius',
                                      1000,4)

        gp4_model, μ_gp4, lg_σ_gp4, Xu4, Xu_er4 = gp.sparse_fully_heteroscedastic_gp(x_train, x_train_er, rad_train, 80, 40)
        gp4_trace = az.from_netcdf('models/model_artifacts/gp_radius.nc') 
        gp4_pred, lpd_GP4 = posterior_predictive_GP(gp4_model, μ_gp4, lg_σ_gp4, 
                                            gp4_trace, X,
                                            X_er,
                                            Xu4, Xu_er4, 4, 'radius')

        
        hbnn4_trace = az.from_netcdf('models/model_artifacts/HBNN_sig_015_15_nodes_radius_4_param.nc')
        hbnn4_pred, lpd_HBNN4 = sample_post_pred_HBNN_para(hbnn4_trace,  
                                                      X,
                                                      X_er,
                                                      15, 4, 'radius')
        
        (bhs_trace, bhs_pred, bhs_w) = run_stack(bart4_pred, hbnn4_pred, gp4_pred,
                                            x_train, X, lpd_BART4, lpd_HBNN4,
                                            lpd_GP4)
        
        
        if test == True:
            mard_BART = mard(unorm_rad, bart4_pred.mean(0))
            mrd_BART = mrd(unorm_rad, bart4_pred.mean(0))
            
            print('MARD BART:', mard_BART)
            print('MRD BART:', mrd_BART)
            
            mard_GP = mard(unorm_rad, gp4_pred.mean(0))
            mrd_GP = mrd(unorm_rad, gp4_pred.mean(0))
            
            print('MARD GP:', mard_GP)
            print('MRD GP:', mrd_GP)
            
            mard_HBNN = mard(unorm_rad, hbnn4_pred.mean(0))
            mrd_HBNN = mrd(unorm_rad, hbnn4_pred.mean(0))
            
            print('MARD HBNN:', mard_HBNN)
            print('MRD HBNN:', mrd_HBNN)
            
            mard_BHS = mard(unorm_rad, bhs_pred.mean(0))
            mrd_BHS = mrd(unorm_rad, bhs_pred.mean(0))
            
            print('MARD BHS:', mard_BHS)
            print('MRD BHS:', mrd_BHS)
            
        return [bart4_pred, gp4_pred, hbnn4_pred], bhs_pred, bhs_w

def predictNAN(X, X_er, target, test=False):
    
    df_train = get_dataset('Datasets/data_sample_calculated_density.txt', 'MS')
    (x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
    mass_test, emass_test
    ) = return_train_test(df_train)
    
    if test == True:
        X = x_test
        X_er = x_test_err
        
    if target == 'mass':
        
        unorm_mass = denormalise_val(mass_test, 'mass')
        
        hbnn4_trace = az.from_netcdf('models/model_artifacts/HBNN_mass.nc')
        hbnn4_pred, lpd_HBNN4 = sample_post_pred_HBNN_para(hbnn4_trace,  
                                                      X,
                                                      X_er,
                                                      15, 4, 'mass')
        
        if test == True:
            mard_HBNN = mard(unorm_mass, hbnn4_pred.mean(0))
            mrd_HBNN = mrd(unorm_mass, hbnn4_pred.mean(0))
        
        return hbnn4_pred
    
    if target == 'radius':
        
        unorm_rad = denormalise_val(rad_test, 'radius')
        
        hbnn4_trace = az.from_netcdf('models/model_artifacts/HBNN_sig_015_15_nodes_radius_4_param.nc')
        hbnn4_pred, lpd_HBNN4 = sample_post_pred_HBNN_para(hbnn4_trace,  
                                                      X,
                                                      X_er,
                                                      15, 4, 'radius')  
        if test == True:
            
            mard_HBNN = mard(unorm_rad, hbnn4_pred.mean(0))
            mrd_HBNN = mrd(unorm_rad, hbnn4_pred.mean(0))
            
            print('MARD HBNN:', mard_HBNN)
            print('MRD HBNN:', mrd_HBNN)
            
        return hbnn4_pred

def predict3(X, X_er, target, test=False): # Default: not test-mode
    
    df_train = get_dataset(TRAINING_FILE, 'MS')
    (x_train, x_train_er, x_test, x_test_err, mass_train, emass_train,
    mass_test, emass_test
    ) = return_train_test(df_train)
    
    
    x_train3 = x_train[['Teff', 'Meta', 'L']]
    x_train3_er = x_train_er[['eTeff', 'eMeta', 'eL']]
    
    if test == True:
        X = x_test[['Teff', 'Meta', 'L']]
        X_er = x_test_err[['eTeff', 'eMeta', 'eL']]
    
    if target == 'mass':
        
        unorm_mass = denormalise_val(mass_test, 'mass')
        
        # CHANGE NAMES HERE OF THE OUTPUT FILES
        bart3_model = bart.BART_M(x_train3,
                                  x_train3_er,
                                  mass_train, emass_train)
        bart3_pred, lpd_BART3 = sample_pred_BART(bart3_model,
                                      X,
                                      X_er, 'mass',
                                      3000, 4,
                                      trace_filename=os.path.join(OUTPUT_DIR, f'BART_mass_3param_L_prediction_3000_draws_4_chains_seed_{SAMPLING_SEED}.nc'),
                                      predictions_filename=os.path.join(OUTPUT_DIR, f'BART_mass_3param_L_prediction_3000_draws_4_chains_predictions_seed_{SAMPLING_SEED}.nc')) # Made 2000 draws bc better MARD on test set

        gp3_model, μ_gp3, lg_σ_gp3, Xu3, Xu_er3 = gp.sparse_fully_heteroscedastic_gp(x_train3,
                                                                                      x_train3_er, 
                                                                                      mass_train, 
                                                                                      80, 40)
        
        # CHANGE NAMES HERE
        # Change gp3_trace and hbnn3_trace according to which training we did

        gp3_trace = az.from_netcdf(os.path.join(OUTPUT_DIR, f'GP_mass_3param_L_1000_draws_4_chains_80_40_seed_{SAMPLING_SEED}.nc'))
        gp3_pred, lpd_GP3 = posterior_predictive_GP(gp3_model, μ_gp3, lg_σ_gp3, 
                                            gp3_trace, X,
                                            X_er,
                                            Xu3, Xu_er3, 3, 'mass')
        
        hbnn3_trace = az.from_netcdf(os.path.join(OUTPUT_DIR, f'HBNN_mass_3param_L_1000_draws_4_chains_15_nodes_sig_015_seed_{SAMPLING_SEED}.nc'))
        hbnn3_pred, lpd_HBNN3 = sample_post_pred_HBNN_para(hbnn3_trace,  
                                                      X,
                                                      X_er,
                                                      15, 3, 'mass')

        (bhs_trace, bhs_pred, bhs_w) = run_stack(bart3_pred, hbnn3_pred, gp3_pred,
                                            x_train3, X, lpd_BART3, lpd_HBNN3,
                                            lpd_GP3,
                                            draws=3000, chains=4)
        bhs_trace.to_netcdf(os.path.join(OUTPUT_DIR, f'BHS_mass_3param_L_prediction_3000_draws_4_chains_seed_{SAMPLING_SEED}.nc'))
        
        if test == True:
            mard_BART = mard(unorm_mass, bart3_pred.mean(0))
            mrd_BART = mrd(unorm_mass, bart3_pred.mean(0))
            
            print('MARD BART:', mard_BART)
            print('MRD BART:', mrd_BART)
            
            mard_GP = mard(unorm_mass, gp3_pred.mean(0))
            mrd_GP = mrd(unorm_mass, gp3_pred.mean(0))
            
            print('MARD GP:', mard_GP)
            print('MRD GP:', mrd_GP)
            
            mard_HBNN = mard(unorm_mass, hbnn3_pred.mean(0))
            mrd_HBNN = mrd(unorm_mass, hbnn3_pred.mean(0))
            
            print('MARD HBNN:', mard_HBNN)
            print('MRD HBNN:', mrd_HBNN)
            
            mard_BHS = mard(unorm_mass, bhs_pred.mean(0))
            mrd_BHS = mrd(unorm_mass, bhs_pred.mean(0))
            
            print('MARD BHS:', mard_BHS)
            print('MRD BHS:', mrd_BHS)

            plot_mass_diagnostics(unorm_mass, bart3_pred, 'BART',
                                  output_base=os.path.join(OUTPUT_DIR, f'BART_mass_3param_L_prediction_seed_{SAMPLING_SEED}'))
            plot_mass_diagnostics(unorm_mass, bhs_pred, 'BHS', filtered_percentiles=(95, 90),
                                  output_base=os.path.join(OUTPUT_DIR, f'BHS_mass_3param_L_prediction_seed_{SAMPLING_SEED}'))
        
        return [bart3_pred, gp3_pred, hbnn3_pred], bhs_pred, bhs_w
    
    if target == 'radius':
        
        unorm_rad = denormalise_val(rad_test, 'radius')
        
        bart3_model = bart.BART_R(x_train3,
                                  x_train3_er,
                                  rad_train, erad_train)
        
        bart3_pred, lpd_BART3 = sample_pred_BART(bart3_model,
                                      X,
                                      X_er, 'radius',
                                      2000, 4) # Made 2000 draws bc better MARD on test set

        gp3_model, μ_gp3, lg_σ_gp3, Xu3, Xu_er3 = gp.sparse_fully_heteroscedastic_gp(x_train3, 
                                                                                     x_train3_er,
                                                                                     rad_train, 80, 40)
        gp3_trace = az.from_netcdf('Train_outputs/GP_radius_3param_1000_draws_80_40.nc')
        gp3_pred, lpd_GP3 = posterior_predictive_GP(gp3_model, μ_gp3, lg_σ_gp3, 
                                            gp3_trace, X,
                                            X_er,
                                            Xu3, Xu_er3, 3, 'radius')
        
        hbnn3_trace = az.from_netcdf('Train_outputs/HBNN_radius_3param_1000_draws_15_nodes_sig_015.nc')
        hbnn3_pred, lpd_HBNN3 = sample_post_pred_HBNN_para(hbnn3_trace,  
                                                      X,
                                                      X_er,
                                                      15, 3, 'radius')

        
        (bhs_trace, bhs_pred, bhs_w) = run_stack(bart3_pred, hbnn3_pred, gp3_pred,
                                            x_train3, X, lpd_BART3, lpd_HBNN3,
                                            lpd_GP3)
        
        if test == True:
            mard_BART = mard(unorm_rad, bart3_pred.mean(0))
            mrd_BART = mrd(unorm_rad, bart3_pred.mean(0))
            
            print('MARD BART:', mard_BART)
            print('MRD BART:', mrd_BART)
            
            mard_GP = mard(unorm_rad, gp3_pred.mean(0))
            mrd_GP = mrd(unorm_rad, gp3_pred.mean(0))
            
            print('MARD GP:', mard_GP)
            print('MRD GP:', mrd_GP)
            
            mard_HBNN = mard(unorm_rad, hbnn3_pred.mean(0))
            mrd_HBNN = mrd(unorm_rad, hbnn3_pred.mean(0))
            
            print('MARD HBNN:', mard_HBNN)
            print('MRD HBNN:', mrd_HBNN)
            
            mard_BHS = mard(unorm_rad, bhs_pred.mean(0))
            mrd_BHS = mrd(unorm_rad, bhs_pred.mean(0))
            
            print('MARD BHS:', mard_BHS)
            print('MRD BHS:', mrd_BHS)
        
        return [bart3_pred, gp3_pred, hbnn3_pred], bhs_pred, bhs_w
        
        
        
        
def main():
    base_preds, bhs_pred, bhs_w = predict3(None, None, 'mass', test=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pd.DataFrame(bhs_pred.mean(0)).to_csv(
        os.path.join(OUTPUT_DIR, "3_features_post_pred_bhs_mass_res.csv"),
        index=False,
    )
    pd.DataFrame(bhs_w.mean(0)).to_csv(
        os.path.join(OUTPUT_DIR, "3_features_post_pred_bhs_mass_w.csv"),
        index=False,
    )

    # X1, X1_er = prepare_pred4("Datasets/dataset_C_trimmed_8cols_NASAFLAG.csv")
    
    # pred1,_ = predict4(X1, X1_er, 'radius', test=True)
    # pred1.to_csv("Results/post_pred_bhs_rad.csv")
    # #w1.to_csv("Results/NASAFLAG_6col_dataC_radius_w.csv")
    
    # pred2,_ = predict4(X1, X1_er, 'mass', test=True)
    # pred2.to_csv("Results/post_pred_bhs_mass.csv")
    # w2.to_csv("Results/NASAFLAG_6col_dataC_mass_w.csv")
    # X2, X2_er = prepare_pred3("Datasets/ARIEL_level_0.csv")
    # print(X2)
    
    # pred, w3 = predict3(X2, X2_er, 'radius', test=True)
    # pred.to_csv("Results/Ariel_radius_pred_lvl0.csv")
    
    # pred, w3 = predict3(X2, X2_er, 'mass', test=True)
    # pred.to_csv("Results/Ariel_mass_pred_lvl0_check.csv")
    #w3.to_csv("Results/Ariel_radius_w_lvl0.csv")
    
    #pred, w4 = predictNAN(X, X_er, 'mass', test=False)
    #pred.to_csv("test_results_4_param_mass_w_hdi.csv")
    #print(pred)
    #w4.to_csv('weights_results_4_param_mass_w_hdi.csv')
    
if __name__ == '__main__':
    main()
    



