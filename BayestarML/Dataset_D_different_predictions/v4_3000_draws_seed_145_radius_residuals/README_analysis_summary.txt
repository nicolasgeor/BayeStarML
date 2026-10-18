Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_3000_draws_seed_145.csv
Input rows: 300
Rows usable before radius cut: 300
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals\plots_before_rad_cut
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

delta_R: n=102, mean=-0.0277381, median=-0.00358927, std=0.133874, min=-0.524874, max=0.311041
frac_residual: n=102, mean=-0.0108285, median=-0.00241314, std=0.0729581, min=-0.268507, max=0.188624
z_R: n=102, mean=-0.405882, median=-0.0589223, std=1.75504, min=-7.63463, max=3.41275
z_R_q68: n=102, mean=-0.411969, median=-0.0592258, std=1.77958, min=-7.67139, max=3.41653
oblateness: n=102, mean=0.0107463, median=0.00277, std=0.0194447, min=4.9e-07, max=0.118
fill_factor: n=102, mean=0.283757, median=0.2517, std=0.195833, min=0.0141, max=0.875
sigma_pred_q68: n=102, mean=0.0590158, median=0.0411327, std=0.049893, min=0.00826708, max=0.23769
rad_sigma: n=102, mean=0.0671605, median=0.0414804, std=0.0902229, min=0.00865962, max=0.802113

68% interval coverage: 0.451
95% interval coverage: 0.706

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 102  -0.208292   0.035657     -0.281577    0.004144     -0.013436         -0.048237
      fill_factor frac_residual 102  -0.134167   0.178816     -0.283218    0.003921     -0.049984          0.003355
log10_fill_factor frac_residual 102  -0.209843   0.034275     -0.283218    0.003921     -0.040629         -0.038258

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_145_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv