Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_2341.csv
Input rows: 295
Rows usable before radius cut: 295
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_2341_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 208
ROBUST: True
Rows before robust cut: 208
Rows after robust cut: 99
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 99

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=99, mean=-0.0320595, median=-0.00731857, std=0.139841, min=-0.535805, max=0.313206
frac_residual: n=99, mean=-0.0127205, median=-0.00519047, std=0.0757172, min=-0.261267, max=0.189937
z_R: n=99, mean=-0.422323, median=-0.0688731, std=1.78632, min=-7.76867, max=3.38235
z_R_q68: n=99, mean=-0.428471, median=-0.0696489, std=1.80339, min=-7.78136, max=3.40576
oblateness: n=99, mean=0.0110354, median=0.00278, std=0.0196657, min=4.9e-07, max=0.118
fill_factor: n=99, mean=0.286937, median=0.2524, std=0.197864, min=0.0141, max=0.875
sigma_pred_q68: n=99, mean=0.0622708, median=0.0462521, std=0.0499888, min=0.00997633, max=0.251674
rad_sigma: n=99, mean=0.0648037, median=0.04635, std=0.0573602, min=0.010098, max=0.318792

68% interval coverage: 0.444
95% interval coverage: 0.727

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 99  -0.273905   0.006081     -0.322407    0.001136     -0.017563         -0.061692
      fill_factor frac_residual 99  -0.178624   0.076899     -0.324289    0.001058     -0.068354          0.006893
log10_fill_factor frac_residual 99  -0.275488   0.005782     -0.324289    0.001058     -0.052974         -0.048574

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_2341_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_2341_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_2341_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv