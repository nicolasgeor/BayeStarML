Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_489.csv
Input rows: 293
Rows usable before radius cut: 293
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_489_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 207
ROBUST: True
Rows before robust cut: 207
Rows after robust cut: 98
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 98

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=98, mean=-0.0314488, median=-0.00598244, std=0.141691, min=-0.550437, max=0.320171
frac_residual: n=98, mean=-0.0127006, median=-0.00419744, std=0.0786551, min=-0.262474, max=0.194161
z_R: n=98, mean=-0.35604, median=-0.0133683, std=1.78757, min=-8.25478, max=3.4549
z_R_q68: n=98, mean=-0.397086, median=-0.125949, std=1.82914, min=-8.28718, max=3.4753
oblateness: n=98, mean=0.011148, median=0.00279, std=0.0197347, min=4.9e-07, max=0.118
fill_factor: n=98, mean=0.289698, median=0.2526, std=0.196956, min=0.0141, max=0.875
sigma_pred_q68: n=98, mean=0.0629704, median=0.0447409, std=0.0525795, min=0.0113873, max=0.257154
rad_sigma: n=98, mean=0.945653, median=0.0450609, std=3.836, min=0.0114344, max=24.4318

68% interval coverage: 0.429
95% interval coverage: 0.724

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 98  -0.230433   0.022447     -0.289273    0.003865     -0.015928         -0.056576
      fill_factor frac_residual 98  -0.148505   0.144464     -0.290709    0.003685     -0.059306          0.004480
log10_fill_factor frac_residual 98  -0.232108   0.021461     -0.290709    0.003685     -0.048136         -0.044735

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_489_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_489_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_489_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv