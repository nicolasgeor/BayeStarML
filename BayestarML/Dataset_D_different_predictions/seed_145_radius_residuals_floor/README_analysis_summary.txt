Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_floor_seed_145.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0454507, median=-0.00627565, std=0.159189, min=-0.846375, max=0.289164
frac_residual: n=102, mean=-0.0215984, median=-0.00441901, std=0.0822713, min=-0.357875, max=0.175357
z_R: n=102, mean=-0.341889, median=-0.0631195, std=1.63169, min=-7.70578, max=4.1706
z_R_q68: n=102, mean=-0.410784, median=-0.116609, std=1.79437, min=-7.9781, max=4.36304
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0519709, median=0.0333195, std=0.0532295, min=0.015204, max=0.284334
rad_sigma: n=102, mean=0.560633, median=0.0362609, std=1.97556, min=0.0168528, max=14.6095

68% interval coverage: 0.343
95% interval coverage: 0.696

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.258389   0.008738     -0.321803    0.000973     -0.018795         -0.073928
      fill_factor frac_residual 102  -0.171668   0.084486     -0.323569    0.000909     -0.072119         -0.001134
log10_fill_factor frac_residual 102  -0.259720   0.008386     -0.323569    0.000909     -0.056704         -0.059881

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv