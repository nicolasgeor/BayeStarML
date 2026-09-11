Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_100_draws_seed_28.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_28_radius_residuals\plots_before_rad_cut
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

delta_R: n=100, mean=-0.00452867, median=-0.0211059, std=0.392343, min=-1.01312, max=2.87544
frac_residual: n=100, mean=0.00134643, median=-0.0148191, std=0.243773, min=-0.668723, max=1.69243
z_R: n=100, mean=-0.814687, median=-0.137614, std=1.93329, min=-7.27568, max=3.31319
z_R_q68: n=100, mean=-0.815076, median=-0.452766, std=2.48965, min=-7.39905, max=9.98147
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0631257, median=0.0412215, std=0.0628015, min=0.00983079, max=0.276516
rad_sigma: n=100, mean=1.59166, median=0.0456629, std=7.15152, min=0.0103643, max=54.2999

68% interval coverage: 0.430
95% interval coverage: 0.710

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.029945   0.767420     -0.203835    0.041938     -0.006180         -0.015961
      fill_factor frac_residual 100  -0.040914   0.686094     -0.204988    0.040767     -0.050392          0.015703
log10_fill_factor frac_residual 100  -0.029752   0.768878     -0.204988    0.040767     -0.018414         -0.011191

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_28_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_28_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_28_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv