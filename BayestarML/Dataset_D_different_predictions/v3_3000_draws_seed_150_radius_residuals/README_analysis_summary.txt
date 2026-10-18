Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_150.csv
Input rows: 301
Rows usable before radius cut: 301
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_150_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 212
ROBUST: True
Rows before robust cut: 212
Rows after robust cut: 103
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 103

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=103, mean=-0.0301842, median=-9.70833e-05, std=0.134697, min=-0.523624, max=0.301158
frac_residual: n=103, mean=-0.0123198, median=-7.36595e-05, std=0.0728741, min=-0.257043, max=0.182631
z_R: n=103, mean=-0.396041, median=-0.00055477, std=1.76995, min=-7.4788, max=3.3942
z_R_q68: n=103, mean=-0.406007, median=-0.000556384, std=1.79752, min=-7.5586, max=3.42566
oblateness: n=103, mean=0.010642, median=0.00276, std=0.019378, min=4.9e-07, max=0.118
fill_factor: n=103, mean=0.281161, median=0.251, std=0.196644, min=0.0141, max=0.875
sigma_pred_q68: n=103, mean=0.0598366, median=0.0427589, std=0.0499473, min=0.00791107, max=0.247458
rad_sigma: n=103, mean=0.133794, median=0.0428563, std=0.565535, min=0.00820885, max=5.59365

68% interval coverage: 0.466
95% interval coverage: 0.728

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 103  -0.223147   0.023469     -0.288451    0.003129     -0.013883         -0.051418
      fill_factor frac_residual 103  -0.153001   0.122846     -0.290155    0.002949     -0.056701          0.003622
log10_fill_factor frac_residual 103  -0.224247   0.022776     -0.290155    0.002949     -0.041837         -0.041015

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_150_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_150_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_150_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv