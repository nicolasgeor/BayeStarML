Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_2805.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2805_radius_residuals\plots_before_rad_cut
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

delta_R: n=100, mean=-0.0452726, median=-0.0258472, std=0.133693, min=-0.510295, max=0.320868
frac_residual: n=100, mean=-0.0250586, median=-0.0178305, std=0.0737239, min=-0.277047, max=0.194583
z_R: n=100, mean=-0.836465, median=-0.290398, std=1.95214, min=-7.73308, max=3.24976
z_R_q68: n=100, mean=-0.852883, median=-0.299203, std=1.98843, min=-8.28169, max=3.21666
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0658221, median=0.0474099, std=0.0556749, min=0.0101691, max=0.272312
rad_sigma: n=100, mean=0.072458, median=0.0481134, std=0.0764305, min=0.0108973, max=0.478907

68% interval coverage: 0.510
95% interval coverage: 0.690

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.189786   0.058594     -0.236586    0.017794     -0.011845         -0.058232
      fill_factor frac_residual 100  -0.108151   0.284143     -0.237968    0.017120     -0.040286         -0.013581
log10_fill_factor frac_residual 100  -0.191253   0.056635     -0.237968    0.017120     -0.035798         -0.049433

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2805_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2805_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2805_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv