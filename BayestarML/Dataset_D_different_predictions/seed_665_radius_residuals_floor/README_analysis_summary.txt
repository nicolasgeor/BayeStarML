Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_floor_seed_665.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0367717, median=-0.00199044, std=0.157912, min=-0.809157, max=0.314459
frac_residual: n=102, mean=-0.0161909, median=-0.00115418, std=0.0824758, min=-0.342138, max=0.190697
z_R: n=102, mean=-0.313437, median=-0.0137858, std=1.90544, min=-8.90391, max=4.33937
z_R_q68: n=102, mean=-0.351013, median=-0.0418274, std=2.07594, min=-9.00389, max=4.51365
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0398317, median=0.0302444, std=0.0284051, min=0.0180926, max=0.158979
rad_sigma: n=102, mean=0.084277, median=0.0317837, std=0.191966, min=0.018741, max=1.46653

68% interval coverage: 0.304
95% interval coverage: 0.627

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.247940   0.011985     -0.305179    0.001815     -0.018079         -0.066530
      fill_factor frac_residual 102  -0.168215   0.091025     -0.306962    0.001701     -0.070844          0.003912
log10_fill_factor frac_residual 102  -0.249455   0.011458     -0.306962    0.001701     -0.054599         -0.053051

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_665_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv