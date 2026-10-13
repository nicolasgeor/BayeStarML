Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_187426.csv
Input rows: 301
Rows usable before radius cut: 301
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_187426_radius_residuals\plots_before_rad_cut
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

delta_R: n=103, mean=-0.0287776, median=0.000589422, std=0.137854, min=-0.54084, max=0.332629
frac_residual: n=103, mean=-0.0116198, median=0.000517037, std=0.0747125, min=-0.263452, max=0.201716
z_R: n=103, mean=-0.385587, median=0.00933248, std=1.78653, min=-8.06566, max=3.58666
z_R_q68: n=103, mean=-0.384905, median=0.00945719, std=1.7963, min=-8.10017, max=3.59169
oblateness: n=103, mean=0.010642, median=0.00276, std=0.019378, min=4.9e-07, max=0.118
fill_factor: n=103, mean=0.281161, median=0.251, std=0.196644, min=0.0141, max=0.875
sigma_pred_q68: n=103, mean=0.0605506, median=0.0441412, std=0.049735, min=0.00856108, max=0.248729
rad_sigma: n=103, mean=0.0611298, median=0.0447481, std=0.0503613, min=0.00881422, max=0.248357

68% interval coverage: 0.466
95% interval coverage: 0.699

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 103  -0.206759   0.036130     -0.275926    0.004785     -0.013188         -0.048760
      fill_factor frac_residual 103  -0.138528   0.162870     -0.277487    0.004543     -0.052632          0.003178
log10_fill_factor frac_residual 103  -0.207791   0.035191     -0.277487    0.004543     -0.039744         -0.038880

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_187426_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_187426_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_187426_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv