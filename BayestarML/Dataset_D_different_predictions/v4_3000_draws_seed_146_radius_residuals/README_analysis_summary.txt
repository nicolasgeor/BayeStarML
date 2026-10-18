Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_146.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0246272, median=-0.00117894, std=0.135404, min=-0.526129, max=0.292934
frac_residual: n=102, mean=-0.00824216, median=-0.000878895, std=0.0737168, min=-0.261323, max=0.177643
z_R: n=102, mean=-0.284313, median=-0.0218213, std=1.71977, min=-7.37782, max=3.20959
z_R_q68: n=102, mean=-0.28254, median=-0.021808, std=1.72557, min=-7.3666, max=3.23753
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.060321, median=0.0410897, std=0.0509177, min=0.0083586, max=0.248167
rad_sigma: n=102, mean=0.0608229, median=0.0412622, std=0.051373, min=0.00855649, max=0.247694

68% interval coverage: 0.422
95% interval coverage: 0.716

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.235414   0.017226     -0.306123    0.001754     -0.015343         -0.050962
      fill_factor frac_residual 102  -0.161142   0.105665     -0.307798    0.001649     -0.060658          0.008970
log10_fill_factor frac_residual 102  -0.236957   0.016489     -0.307798    0.001649     -0.046355         -0.039537

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv