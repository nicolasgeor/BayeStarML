Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_1684.csv
Input rows: 293
Rows usable before radius cut: 293
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_1684_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 207
ROBUST: True
Rows before robust cut: 207
Rows after robust cut: 98
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 98

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=98, mean=-0.0267288, median=-0.00342798, std=0.428913, min=-3.02394, max=1.87701
frac_residual: n=98, mean=-0.000335263, median=-0.00223258, std=0.316774, min=-1.94967, max=1.65813
z_R: n=98, mean=-0.362542, median=-0.011283, std=1.77672, min=-8.07174, max=3.49202
z_R_q68: n=98, mean=-0.373501, median=-0.057547, std=2.49969, min=-12.367, max=8.30004
oblateness: n=98, mean=0.011148, median=0.00279, std=0.0197347, min=4.9e-07, max=0.118
fill_factor: n=98, mean=0.289698, median=0.2526, std=0.196956, min=0.0141, max=0.875
sigma_pred_q68: n=98, mean=0.0599653, median=0.0423072, std=0.0527246, min=0.0114407, max=0.25318
rad_sigma: n=98, mean=3.98377, median=0.0447654, std=20.1556, min=0.0117506, max=172.887

68% interval coverage: 0.408
95% interval coverage: 0.714

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 98  -0.043599   0.669912     -0.254883    0.011315     -0.012137         -0.033768
      fill_factor frac_residual 98  -0.039873   0.696672     -0.256345    0.010839     -0.064130          0.018243
log10_fill_factor frac_residual 98  -0.045066   0.659482     -0.256345    0.010839     -0.037640         -0.025385

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_1684_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_1684_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_1684_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv