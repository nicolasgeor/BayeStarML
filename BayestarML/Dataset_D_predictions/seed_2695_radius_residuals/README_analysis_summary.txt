Input file: Dataset_D_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_2695.csv
Input rows: 297
Rows usable before radius cut: 297
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2695_radius_residuals\plots_before_rad_cut
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

delta_R: n=100, mean=-0.0546629, median=-0.0229561, std=0.16525, min=-1.0379, max=0.317383
frac_residual: n=100, mean=-0.031716, median=-0.0161098, std=0.10054, min=-0.714806, max=0.19247
z_R: n=100, mean=-0.828449, median=-0.297616, std=1.942, min=-8.18862, max=3.29309
z_R_q68: n=100, mean=-0.864206, median=-0.316397, std=1.98239, min=-8.37366, max=3.16692
oblateness: n=100, mean=0.010926, median=0.00277, std=0.0195967, min=4.9e-07, max=0.118
fill_factor: n=100, mean=0.284894, median=0.2517, std=0.19792, min=0.0141, max=0.875
sigma_pred_q68: n=100, mean=0.0663115, median=0.0467371, std=0.0570217, min=0.0105888, max=0.291318
rad_sigma: n=100, mean=0.300697, median=0.0475032, std=2.29525, min=0.0108301, max=23.0101

68% interval coverage: 0.530
95% interval coverage: 0.670

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 100  -0.149036   0.138901     -0.216202    0.030737     -0.012685         -0.067242
      fill_factor frac_residual 100  -0.060441   0.550266     -0.217254    0.029914     -0.030703         -0.022969
log10_fill_factor frac_residual 100  -0.150001   0.136332     -0.217254    0.029914     -0.038290         -0.057786

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2695_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2695_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed_2695_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv