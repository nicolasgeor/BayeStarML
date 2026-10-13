Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_6987.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_6987_radius_residuals\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0291497, median=-0.00186485, std=0.137396, min=-0.513124, max=0.293865
frac_residual: n=102, mean=-0.011376, median=-0.00124315, std=0.0756264, min=-0.255966, max=0.178208
z_R: n=102, mean=-0.331687, median=-0.0124516, std=1.64774, min=-7.19938, max=3.22654
z_R_q68: n=102, mean=-0.361956, median=-0.0560533, std=1.69514, min=-7.27026, max=3.21428
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0606593, median=0.0418476, std=0.0521931, min=0.00907481, max=0.252786
rad_sigma: n=102, mean=0.415336, median=0.0413807, std=1.31126, min=0.0090926, max=9.799

68% interval coverage: 0.461
95% interval coverage: 0.725

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.249148   0.011563     -0.326694    0.000805     -0.016659         -0.057759
      fill_factor frac_residual 102  -0.181923   0.067251     -0.328618    0.000746     -0.070255          0.008559
log10_fill_factor frac_residual 102  -0.250727   0.011030     -0.328618    0.000746     -0.050320         -0.045348

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_6987_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_6987_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_6987_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv