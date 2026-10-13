Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_664.csv
Input rows: 295
Rows usable before radius cut: 295
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_664_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 208
ROBUST: True
Rows before robust cut: 208
Rows after robust cut: 99
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 99

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=99, mean=-0.027037, median=0.0019392, std=0.140335, min=-0.526289, max=0.334428
frac_residual: n=99, mean=-0.00951257, median=0.00127579, std=0.0770774, min=-0.267395, max=0.202806
z_R: n=99, mean=-0.296235, median=0.0120569, std=1.71522, min=-7.69874, max=3.61335
z_R_q68: n=99, mean=-0.297409, median=0.0120627, std=1.73138, min=-7.72715, max=3.64063
oblateness: n=99, mean=0.0110354, median=0.00278, std=0.0196657, min=4.9e-07, max=0.118
fill_factor: n=99, mean=0.286937, median=0.2524, std=0.197864, min=0.0141, max=0.875
sigma_pred_q68: n=99, mean=0.0637235, median=0.0454556, std=0.0495774, min=0.0135815, max=0.248431
rad_sigma: n=99, mean=0.0723916, median=0.0459049, std=0.077821, min=0.0140033, max=0.546175

68% interval coverage: 0.404
95% interval coverage: 0.727

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 99  -0.262232   0.008739     -0.307280    0.001976     -0.017116         -0.057240
      fill_factor frac_residual 99  -0.165677   0.101239     -0.308853    0.001868     -0.064539          0.009006
log10_fill_factor frac_residual 99  -0.263871   0.008313     -0.308853    0.001868     -0.051651         -0.044471

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_664_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_664_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_664_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv