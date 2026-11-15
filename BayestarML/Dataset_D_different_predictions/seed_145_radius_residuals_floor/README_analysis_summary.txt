Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_floor_seed_145.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 211
ROBUST: True
Rows before robust cut: 211
Rows after robust cut: 102
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 102

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=102, mean=-0.0462547, median=-0.00489629, std=0.161047, min=-0.874503, max=0.285722
frac_residual: n=102, mean=-0.0220115, median=-0.00324235, std=0.0829133, min=-0.369769, max=0.17327
z_R: n=102, mean=-0.348376, median=-0.0573649, std=1.64795, min=-8.01075, max=4.14891
z_R_q68: n=102, mean=-0.415959, median=-0.127116, std=1.80714, min=-8.14503, max=4.33923
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0513332, median=0.0327771, std=0.0528979, min=0.0144007, max=0.286201
rad_sigma: n=102, mean=0.521562, median=0.0362175, std=1.74626, min=0.0161558, max=12.1844

68% interval coverage: 0.353
95% interval coverage: 0.716

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.258156   0.008801     -0.325738    0.000835     -0.018924         -0.074702
      fill_factor frac_residual 102  -0.173304   0.081523     -0.327504    0.000779     -0.073375         -0.001191
log10_fill_factor frac_residual 102  -0.259440   0.008459     -0.327504    0.000779     -0.057085         -0.060551

Each model on its own (BHS is the stack; trend = Spearman rho with log10 oblateness):
model   n  MARD_percent  median_abs_frac_residual_percent  mean_frac_residual_percent  coverage_68  coverage_95  median_half_width_68  spearman_rho_frac_residual  spearman_p_frac_residual  spearman_rho_abs_frac_residual  spearman_p_abs_frac_residual
  BHS 102         5.704                              3.96                      -2.201       0.3529       0.7157               0.03278                     -0.3257                 0.0008352                          0.3339                     0.0006041
 BART 102         5.354                             4.039                      -2.137       0.6863        0.902               0.07482                     -0.3818                 7.494e-05                          0.3587                      0.000214
 HBNN 102         5.084                             3.623                     -0.8645       0.4706       0.7549               0.04265                     -0.2682                  0.006429                          0.2504                       0.01112
   GP 102         5.995                             4.073                      -2.356       0.3824       0.7647               0.03634                     -0.3244                  0.000879                          0.3349                     0.0005808

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv