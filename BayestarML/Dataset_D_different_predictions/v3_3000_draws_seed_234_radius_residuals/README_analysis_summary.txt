Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_234.csv
Input rows: 301
Rows usable before radius cut: 301
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_234_radius_residuals\plots_before_rad_cut
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

delta_R: n=103, mean=-0.0313855, median=-0.00286364, std=0.137146, min=-0.540986, max=0.315023
frac_residual: n=103, mean=-0.0128394, median=-0.0019614, std=0.0751172, min=-0.267734, max=0.191039
z_R: n=103, mean=-0.402291, median=-0.0250234, std=1.72826, min=-7.84019, max=3.42384
z_R_q68: n=103, mean=-0.413273, median=-0.0637239, std=1.76344, min=-7.90609, max=3.45011
oblateness: n=103, mean=0.010642, median=0.00276, std=0.019378, min=4.9e-07, max=0.118
fill_factor: n=103, mean=0.281161, median=0.251, std=0.196644, min=0.0141, max=0.875
sigma_pred_q68: n=103, mean=0.0589316, median=0.0404898, std=0.049838, min=0.00815513, max=0.244643
rad_sigma: n=103, mean=0.303484, median=0.0411685, std=1.58313, min=0.00852327, max=15.2014

68% interval coverage: 0.447
95% interval coverage: 0.709

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 103  -0.222646   0.023791     -0.288446    0.003129     -0.014278         -0.053050
      fill_factor frac_residual 103  -0.146213   0.140557     -0.290117    0.002952     -0.055853          0.002864
log10_fill_factor frac_residual 103  -0.223967   0.022951     -0.290117    0.002952     -0.043070         -0.042381

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_234_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_234_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_234_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv