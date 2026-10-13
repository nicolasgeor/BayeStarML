Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_665.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0260465, median=0.00183373, std=0.135576, min=-0.532686, max=0.303731
frac_residual: n=102, mean=-0.0095199, median=0.00134089, std=0.0736129, min=-0.259401, max=0.184191
z_R: n=102, mean=-0.328903, median=0.0506807, std=1.80694, min=-7.75355, max=3.34356
z_R_q68: n=102, mean=-0.333534, median=0.0511921, std=1.83591, min=-7.8217, max=3.36509
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0588778, median=0.042489, std=0.0483674, min=0.00882375, max=0.244485
rad_sigma: n=102, mean=0.0598039, median=0.0431667, std=0.0493655, min=0.00897556, max=0.245648

68% interval coverage: 0.471
95% interval coverage: 0.667

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.215466   0.029638     -0.274673    0.005209     -0.014023         -0.048565
      fill_factor frac_residual 102  -0.139376   0.162379     -0.276229    0.004950     -0.052391          0.005346
log10_fill_factor frac_residual 102  -0.216858   0.028576     -0.276229    0.004950     -0.042364         -0.038120

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv