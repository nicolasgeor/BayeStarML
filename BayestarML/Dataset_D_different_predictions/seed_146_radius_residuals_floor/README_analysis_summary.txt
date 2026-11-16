Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_floor_seed_146.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals_floor\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0402049, median=-0.000880256, std=0.166249, min=-0.929242, max=0.295936
frac_residual: n=102, mean=-0.0178993, median=-0.000593791, std=0.0862546, min=-0.392914, max=0.179464
z_R: n=102, mean=-0.276526, median=-0.0212123, std=1.72365, min=-8.32666, max=3.71142
z_R_q68: n=102, mean=-0.358759, median=-0.0372641, std=1.9335, min=-8.51212, max=3.83797
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0440516, median=0.0313255, std=0.0348778, min=0.0182828, max=0.200755
rad_sigma: n=102, mean=0.163203, median=0.0334454, std=0.489138, min=0.0194779, max=3.15732

68% interval coverage: 0.343
95% interval coverage: 0.608

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.264595   0.007201     -0.329465    0.000721     -0.020178         -0.074081
      fill_factor frac_residual 102  -0.181303   0.068205     -0.331406    0.000668     -0.079855          0.004760
log10_fill_factor frac_residual 102  -0.265943   0.006900     -0.331406    0.000668     -0.060874         -0.058997

Each model on its own (BHS is the stack; trend = Spearman rho with log10 oblateness):
model   n  MARD_percent  median_abs_frac_residual_percent  mean_frac_residual_percent  coverage_68  coverage_95  median_half_width_68  spearman_rho_frac_residual  spearman_p_frac_residual  spearman_rho_abs_frac_residual  spearman_p_abs_frac_residual
  BHS 102         5.881                             4.294                       -1.79       0.3431       0.6078               0.03133                     -0.3295                 0.0007213                          0.2627                      0.007631
 BART 102         5.578                             4.415                     -0.7522       0.7157       0.9216               0.08064                     -0.3752                  0.000102                           0.127                        0.2034
 HBNN 102         5.112                             3.717                      -0.661       0.4314       0.7353               0.04126                     -0.2834                  0.003895                          0.2211                       0.02552
   GP 102         6.128                              4.45                      -1.993       0.3922       0.6569               0.03673                      -0.336                 0.0005551                          0.2636                      0.007434

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_146_radius_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv