Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_20_draws_seed_233.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_233_radius_residuals\plots_before_rad_cut
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

delta_R: n=100, mean=-0.167661, median=-0.0667693, std=1.35877, min=-9.99468, max=7.28463
frac_residual: n=100, mean=-0.0748838, median=-0.0456932, std=0.935312, min=-5.31067, max=6.6224
z_R: n=100, mean=-1.8751, median=-0.970444, std=2.90212, min=-13.2566, max=3.65466
z_R_q68: n=100, mean=-2.42874, median=-1.31732, std=5.12829, min=-29.2458, max=21.5256
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0614842, median=0.0324106, std=0.0747263, min=0.00759338, max=0.346492
rad_sigma: n=100, mean=2.6741, median=0.0361658, std=12.0989, min=0.00925858, max=90.7886

68% interval coverage: 0.260
95% interval coverage: 0.600

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.039041   0.699757      -0.21622    0.030723     -0.030913         -0.161459
      fill_factor frac_residual 100  -0.009711   0.923610      -0.21717    0.029979     -0.045890         -0.061810
log10_fill_factor frac_residual 100  -0.038683   0.702383      -0.21717    0.029979     -0.091858         -0.137428

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_233_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_233_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_233_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv