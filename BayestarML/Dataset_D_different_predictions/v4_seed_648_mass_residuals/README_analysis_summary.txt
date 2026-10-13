Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_1000_draws_seed_648.csv
Input rows: 300
Rows usable before mass cut: 300
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals\plots_before_mass_cut
Mass window: 0.950 <= M <= 1.500 solar masses
Rows after mass window: 140
ROBUST: True
Rows before robust cut: 140
Rows after robust cut: 87
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 87

Residual definitions:
  delta_M = mass_pred - M
  frac_residual = (mass_pred - M) / M
  sigma_delta_M = sqrt(mass_sigma^2 + sigma_M_true^2)
  z_M = delta_M / sigma_delta_M

delta_M: n=87, mean=-0.00855191, median=0.00119056, std=0.121426, min=-0.429803, max=0.428192
frac_residual: n=87, mean=-0.00292519, median=0.00115365, std=0.101435, min=-0.289235, max=0.417748
z_M: n=87, mean=-0.316638, median=0.0320901, std=2.5821, min=-9.51587, max=7.25216
z_M_q68: n=87, mean=-0.366301, median=0.0322062, std=2.78592, min=-9.87096, max=7.51336
oblateness: n=87, mean=0.00964821, median=0.002431, std=0.0186594, min=4.9e-07, max=0.118
fill_factor: n=87, mean=0.27079, median=0.2386, std=0.189812, min=0.0141, max=0.875
sigma_pred_q68: n=87, mean=0.0389637, median=0.0370179, std=0.0107981, min=0.0202313, max=0.0737044
mass_sigma: n=87, mean=0.0497304, median=0.0416077, std=0.0418572, min=0.0224326, max=0.344871

68% interval coverage: 0.333
95% interval coverage: 0.586

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 87  -0.063425   0.559474     -0.142087    0.189249     -0.005677         -0.019089
      fill_factor frac_residual 87   0.028741   0.791583     -0.139737    0.196747      0.015359         -0.007084
log10_fill_factor frac_residual 87  -0.064374   0.553604     -0.139737    0.196747     -0.017298         -0.014963

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-mass-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv