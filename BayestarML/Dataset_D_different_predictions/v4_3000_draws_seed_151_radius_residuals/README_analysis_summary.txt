Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_151.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_151_radius_residuals\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0297365, median=-0.00458866, std=0.134945, min=-0.523935, max=0.293367
frac_residual: n=102, mean=-0.0120061, median=-0.00323576, std=0.0733383, min=-0.264133, max=0.177906
z_R: n=102, mean=-0.405782, median=-0.0218881, std=1.71296, min=-7.87437, max=3.29398
z_R_q68: n=102, mean=-0.406481, median=-0.0529288, std=1.73304, min=-7.93414, max=3.3234
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.060531, median=0.0419819, std=0.0521564, min=0.00748052, max=0.24958
rad_sigma: n=102, mean=0.139883, median=0.042204, std=0.465405, min=0.00749706, max=3.84193

68% interval coverage: 0.451
95% interval coverage: 0.716

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.233364   0.018250     -0.301927    0.002042     -0.015131         -0.054136
      fill_factor frac_residual 102  -0.160119   0.107927     -0.303874    0.001903     -0.059964          0.005009
log10_fill_factor frac_residual 102  -0.234840   0.017508     -0.303874    0.001903     -0.045705         -0.042863

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_151_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_151_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_151_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv