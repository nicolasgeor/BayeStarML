Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_4869.csv
Input rows: 293
Rows usable before radius cut: 293
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4869_radius_residuals\plots_before_rad_cut
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

delta_R: n=98, mean=-0.0304011, median=-0.000670658, std=0.140363, min=-0.530692, max=0.314553
frac_residual: n=98, mean=-0.0119437, median=-0.000490071, std=0.0760622, min=-0.261554, max=0.190754
z_R: n=98, mean=-0.379431, median=-0.00504433, std=1.76257, min=-7.78097, max=3.43136
z_R_q68: n=98, mean=-0.388809, median=-0.00508121, std=1.80421, min=-7.90319, max=3.43465
oblateness: n=98, mean=0.011148, median=0.00279, std=0.0197347, min=4.9e-07, max=0.118
fill_factor: n=98, mean=0.289698, median=0.2526, std=0.196956, min=0.0141, max=0.875
sigma_pred_q68: n=98, mean=0.0617742, median=0.0453849, std=0.0492985, min=0.0124082, max=0.250491
rad_sigma: n=98, mean=0.169901, median=0.0459252, std=0.651245, min=0.0126206, max=5.46564

68% interval coverage: 0.449
95% interval coverage: 0.714

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 98  -0.228602   0.023569     -0.289878    0.003788     -0.015280         -0.054036
      fill_factor frac_residual 98  -0.147877   0.146189     -0.291111    0.003636     -0.057108          0.004600
log10_fill_factor frac_residual 98  -0.230080   0.022660     -0.291111    0.003636     -0.046143         -0.042651

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4869_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4869_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_4869_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv