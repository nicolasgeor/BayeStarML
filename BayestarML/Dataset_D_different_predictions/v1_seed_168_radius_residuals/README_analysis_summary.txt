Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_168.csv
Input rows: 295
Rows usable before radius cut: 295
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_168_radius_residuals\plots_before_rad_cut
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

delta_R: n=99, mean=-0.0297427, median=-0.00552328, std=0.136268, min=-0.518276, max=0.311959
frac_residual: n=99, mean=-0.0118248, median=-0.00297681, std=0.0743241, min=-0.260776, max=0.189181
z_R: n=99, mean=-0.408253, median=-0.0328766, std=1.77465, min=-7.56052, max=3.42276
z_R_q68: n=99, mean=-0.411569, median=-0.0439895, std=1.78966, min=-7.61473, max=3.4539
oblateness: n=99, mean=0.0110354, median=0.00278, std=0.0196657, min=4.9e-07, max=0.118
fill_factor: n=99, mean=0.286937, median=0.2524, std=0.197864, min=0.0141, max=0.875
sigma_pred_q68: n=99, mean=0.0609767, median=0.0430648, std=0.0481019, min=0.0106951, max=0.228332
rad_sigma: n=99, mean=0.0642813, median=0.0448514, std=0.0568108, min=0.0109091, max=0.332576

68% interval coverage: 0.444
95% interval coverage: 0.727

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 99  -0.248448   0.013152     -0.300953    0.002471     -0.015637         -0.055428
      fill_factor frac_residual 99  -0.156172   0.122674     -0.302390    0.002349     -0.058663          0.005008
log10_fill_factor frac_residual 99  -0.249977   0.012581     -0.302390    0.002349     -0.047184         -0.043759

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_168_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_168_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_168_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv