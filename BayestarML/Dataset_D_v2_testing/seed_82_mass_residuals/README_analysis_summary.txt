Input file: Dataset_D_v2_testing\EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_82.csv
Input rows: 297
Rows usable before mass cut: 297
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_v2_testing\seed_82_mass_residuals\plots_before_mass_cut
Mass window: 0.950 <= M <= 1.500 solar masses
Rows after mass window: 139
ROBUST: True
Rows before robust cut: 139
Rows after robust cut: 85
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 85

Residual definitions:
  delta_M = mass_pred - M
  frac_residual = (mass_pred - M) / M
  sigma_delta_M = sqrt(mass_sigma^2 + sigma_M_true^2)
  z_M = delta_M / sigma_delta_M

delta_M: n=85, mean=-0.0157484, median=0.000615408, std=0.127912, min=-0.443632, max=0.450751
frac_residual: n=85, mean=-0.00857674, median=0.000435533, std=0.106218, min=-0.298541, max=0.439757
z_M: n=85, mean=-0.306583, median=0.00664542, std=2.06436, min=-6.75101, max=4.22784
z_M_q68: n=85, mean=-0.46553, median=0.0148761, std=2.73446, min=-9.02924, max=7.28022
oblateness: n=85, mean=0.00983378, median=0.002431, std=0.0188387, min=4.9e-07, max=0.118
fill_factor: n=85, mean=0.271823, median=0.2386, std=0.192285, min=0.0141, max=0.875
sigma_pred_q68: n=85, mean=0.0455667, median=0.0387673, std=0.0224099, min=0.0139933, max=0.116193
mass_sigma: n=85, mean=0.633999, median=0.0583709, std=2.39992, min=0.0152229, max=19.1333

68% interval coverage: 0.353
95% interval coverage: 0.706

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 85  -0.057272   0.602627     -0.113593    0.300613     -0.005108         -0.023225
      fill_factor frac_residual 85   0.044070   0.688803     -0.112978    0.303252      0.024344         -0.015194
log10_fill_factor frac_residual 85  -0.058418   0.595370     -0.112978    0.303252     -0.015626         -0.019565

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_v2_testing\seed_82_mass_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_v2_testing\seed_82_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-mass-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_v2_testing\seed_82_mass_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv