Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_149.csv
Input rows: 301
Rows usable before radius cut: 301
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_149_radius_residuals\plots_before_rad_cut
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

delta_R: n=103, mean=-0.0315563, median=-0.00542425, std=0.137391, min=-0.549903, max=0.316908
frac_residual: n=103, mean=-0.0132368, median=-0.00348964, std=0.0740263, min=-0.264515, max=0.192182
z_R: n=103, mean=-0.43819, median=-0.100313, std=1.84754, min=-8.10294, max=3.44035
z_R_q68: n=103, mean=-0.44348, median=-0.125716, std=1.86954, min=-8.16994, max=3.42398
oblateness: n=103, mean=0.010642, median=0.00276, std=0.019378, min=4.9e-07, max=0.118
fill_factor: n=103, mean=0.281161, median=0.251, std=0.196644, min=0.0141, max=0.875
sigma_pred_q68: n=103, mean=0.0595761, median=0.0434769, std=0.0500272, min=0.00766818, max=0.247896
rad_sigma: n=103, mean=0.0703301, median=0.043978, std=0.0974899, min=0.0080597, max=0.797368

68% interval coverage: 0.447
95% interval coverage: 0.709

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 103  -0.229392   0.019762     -0.302564    0.001894     -0.014497         -0.054065
      fill_factor frac_residual 103  -0.157759   0.111492     -0.304252    0.001781     -0.059388          0.003461
log10_fill_factor frac_residual 103  -0.230528   0.019145     -0.304252    0.001781     -0.043688         -0.043203

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_149_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_149_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_149_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv