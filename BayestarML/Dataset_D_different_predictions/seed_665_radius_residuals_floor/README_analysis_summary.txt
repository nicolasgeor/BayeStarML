Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_floor_seed_665.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0379153, median=-0.000676182, std=0.157327, min=-0.807938, max=0.308982
frac_residual: n=102, mean=-0.0169138, median=-0.000451537, std=0.0820039, min=-0.341623, max=0.187375
z_R: n=102, mean=-0.335478, median=0.0149642, std=1.87633, min=-8.84212, max=4.20945
z_R_q68: n=102, mean=-0.37909, median=-0.00767407, std=2.06329, min=-9.01195, max=4.39145
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0410867, median=0.0318248, std=0.0293952, min=0.0182993, max=0.159559
rad_sigma: n=102, mean=0.0839054, median=0.0348233, std=0.183956, min=0.0193344, max=1.30801

68% interval coverage: 0.314
95% interval coverage: 0.608

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.249756   0.011355     -0.303788    0.001909     -0.018108         -0.067331
      fill_factor frac_residual 102  -0.169960   0.087673     -0.305491    0.001795     -0.071170          0.003281
log10_fill_factor frac_residual 102  -0.251281   0.010848     -0.305491    0.001795     -0.054684         -0.053832

Each model on its own (BHS is the stack; trend = Spearman rho with log10 oblateness):
model   n  MARD_percent  median_abs_frac_residual_percent  mean_frac_residual_percent  coverage_68  coverage_95  median_half_width_68  spearman_rho_frac_residual  spearman_p_frac_residual  spearman_rho_abs_frac_residual  spearman_p_abs_frac_residual
  BHS 102         5.708                             3.829                      -1.691       0.3137       0.6078               0.03182                     -0.3038                  0.001909                          0.2409                       0.01471
 BART 102         5.213                             4.253                      -1.388       0.7745       0.9216               0.08743                     -0.2528                   0.01037                          0.2373                       0.01633
 HBNN 102         5.144                             3.634                     -0.6911       0.4608       0.7353               0.04269                     -0.2586                  0.008681                          0.2319                       0.01902
   GP 102         5.985                             4.077                      -1.812       0.3137       0.6275               0.03287                     -0.3182                  0.001117                          0.2473                       0.01223

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv