Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_1000_draws_seed_38.csv
Input rows: 301
Rows usable before mass cut: 301
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_38_mass_residuals\plots_before_mass_cut
Mass window: 0.950 <= M <= 1.500 solar masses
Rows after mass window: 141
ROBUST: True
Rows before robust cut: 141
Rows after robust cut: 88
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 88

Residual definitions:
  delta_M = mass_pred - M
  frac_residual = (mass_pred - M) / M
  sigma_delta_M = sqrt(mass_sigma^2 + sigma_M_true^2)
  z_M = delta_M / sigma_delta_M

delta_M: n=88, mean=-0.00808441, median=-0.00051097, std=0.117877, min=-0.42613, max=0.430087
frac_residual: n=88, mean=-0.00260431, median=-0.000451588, std=0.0981655, min=-0.286763, max=0.419597
z_M: n=88, mean=-0.304918, median=-0.0159088, std=2.57724, min=-9.86562, max=7.898
z_M_q68: n=88, mean=-0.32961, median=-0.0170437, std=2.74732, min=-10.2468, max=8.17277
oblateness: n=88, mean=0.00953858, median=0.0023155, std=0.0185803, min=4.9e-07, max=0.118
fill_factor: n=88, mean=0.267899, median=0.236005, std=0.190657, min=0.0141, max=0.875
sigma_pred_q68: n=88, mean=0.0395764, median=0.0373949, std=0.00930691, min=0.0251715, max=0.0659003
mass_sigma: n=88, mean=0.0441882, median=0.0426011, std=0.0155055, min=0.0266153, max=0.127967

68% interval coverage: 0.386
95% interval coverage: 0.682

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 88  -0.050566   0.639881     -0.139975    0.193355     -0.004213         -0.014755
      fill_factor frac_residual 88   0.041226   0.702934     -0.137431    0.201655      0.021226         -0.008291
log10_fill_factor frac_residual 88  -0.051423   0.634209     -0.137431    0.201655     -0.012849         -0.011705

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_38_mass_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_38_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-mass-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_38_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv