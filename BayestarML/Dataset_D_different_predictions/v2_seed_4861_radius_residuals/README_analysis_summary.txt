Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_4861.csv
Input rows: 293
Rows usable before radius cut: 293
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4861_radius_residuals\plots_before_rad_cut
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

delta_R: n=98, mean=-0.0316737, median=-0.00308809, std=0.136715, min=-0.514601, max=0.286195
frac_residual: n=98, mean=-0.0130185, median=-0.00216448, std=0.0736953, min=-0.252585, max=0.173557
z_R: n=98, mean=-0.399886, median=-0.0407058, std=1.66943, min=-7.00197, max=3.13992
z_R_q68: n=98, mean=-0.401931, median=-0.0407706, std=1.68376, min=-7.00066, max=3.17378
oblateness: n=98, mean=0.011148, median=0.00279, std=0.0197347, min=4.9e-07, max=0.118
fill_factor: n=98, mean=0.289698, median=0.2526, std=0.196956, min=0.0141, max=0.875
sigma_pred_q68: n=98, mean=0.0626389, median=0.0456444, std=0.0503804, min=0.0107989, max=0.255732
rad_sigma: n=98, mean=0.0648188, median=0.0464187, std=0.0561552, min=0.0110454, max=0.330444

68% interval coverage: 0.490
95% interval coverage: 0.735

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 98  -0.236372   0.019117     -0.294239    0.003273     -0.015308         -0.055187
      fill_factor frac_residual 98  -0.159114   0.117600     -0.296288    0.003054     -0.059536          0.004229
log10_fill_factor frac_residual 98  -0.237884   0.018340     -0.296288    0.003054     -0.046223         -0.043780

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4861_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4861_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4861_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv