Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_1000_draws_floor_seed_648.csv
Input rows: 300
Rows usable before mass cut: 300
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals_floor\plots_before_mass_cut
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

delta_M: n=87, mean=-0.0074129, median=0.00062153, std=0.122547, min=-0.430077, max=0.439477
frac_residual: n=87, mean=-0.00211328, median=0.000551981, std=0.102372, min=-0.289419, max=0.428758
z_M: n=87, mean=-0.2495, median=0.00760349, std=2.24214, min=-8.3992, max=6.08936
z_M_q68: n=87, mean=-0.287576, median=0.00761639, std=2.45637, min=-8.71058, max=6.74357
oblateness: n=87, mean=0.00964821, median=0.002431, std=0.0186594, min=4.9e-07, max=0.118
fill_factor: n=87, mean=0.27079, median=0.2386, std=0.189812, min=0.0141, max=0.875
sigma_pred_q68: n=87, mean=0.0447036, median=0.0421783, std=0.0135605, min=0.0225283, max=0.0829255
mass_sigma: n=87, mean=0.058709, median=0.0445458, std=0.0502052, min=0.024242, max=0.369719

68% interval coverage: 0.356
95% interval coverage: 0.655

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 87  -0.061025   0.574458     -0.127097    0.240758     -0.005513         -0.017809
      fill_factor frac_residual 87   0.028233   0.795187     -0.124774    0.249532      0.015227         -0.006237
log10_fill_factor frac_residual 87  -0.062020   0.568225     -0.124774    0.249532     -0.016819         -0.013818

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals_floor\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-mass-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_648_mass_residuals_floor\EB_plot_binned_residuals_vs_log10_oblateness_before_mass_cut.csv