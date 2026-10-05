Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_239.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_239_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 210
ROBUST: True
Rows before robust cut: 210
Rows after robust cut: 100
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 100

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=100, mean=-0.0516436, median=-0.0280427, std=0.135902, min=-0.52793, max=0.325556
frac_residual: n=100, mean=-0.0291966, median=-0.019381, std=0.0753934, min=-0.276004, max=0.197426
z_R: n=100, mean=-0.927294, median=-0.332583, std=2.13542, min=-8.75184, max=3.53217
z_R_q68: n=100, mean=-0.943269, median=-0.367322, std=2.16943, min=-8.80409, max=3.59058
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0668621, median=0.0477365, std=0.0546352, min=0.0109393, max=0.263928
rad_sigma: n=100, mean=0.141852, median=0.0473113, std=0.551522, min=0.0110593, max=5.37676

68% interval coverage: 0.490
95% interval coverage: 0.690

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.199065   0.047085     -0.239785    0.016267     -0.012705         -0.064780
      fill_factor frac_residual 100  -0.108825   0.281135     -0.240596    0.015898     -0.041455         -0.017386
log10_fill_factor frac_residual 100  -0.200151   0.045869     -0.240596    0.015898     -0.038312         -0.055282

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_239_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_239_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_239_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv