Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_20_draws_seed_2334.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2334_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 210
ROBUST: True
Rows before robust cut: 210
Rows after robust cut: 100
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 100

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=100, mean=-0.0222483, median=-0.00889507, std=0.284077, min=-1.08892, max=1.92097
frac_residual: n=100, mean=-0.00281736, median=-0.00659397, std=0.199727, min=-0.732294, max=1.47767
z_R: n=100, mean=-0.435631, median=-0.107669, std=2.04272, min=-8.21828, max=4.60845
z_R_q68: n=100, mean=-0.428324, median=-0.172281, std=2.56596, min=-8.60259, max=8.24202
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0422466, median=0.0315413, std=0.0357996, min=0.0118304, max=0.173476
rad_sigma: n=100, mean=0.423711, median=0.0360075, std=2.00673, min=0.0125445, max=15.3512

68% interval coverage: 0.340
95% interval coverage: 0.620

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.067270   0.506055     -0.316017    0.001360     -0.011374         -0.034672
      fill_factor frac_residual 100  -0.062291   0.538107     -0.317513    0.001287     -0.062860          0.015091
log10_fill_factor frac_residual 100  -0.068624   0.497508     -0.317513    0.001287     -0.034799         -0.026511

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2334_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2334_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2334_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv