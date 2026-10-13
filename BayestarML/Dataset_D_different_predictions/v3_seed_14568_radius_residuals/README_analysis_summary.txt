Input file: Dataset_D_different_predictions\EB_oblateness_fill_factor_radius_predictions_4_features_1000_draws_seed_14568.csv
Input rows: 301
Rows usable before radius cut: 301
Pre-radius-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_14568_radius_residuals\plots_before_rad_cut
Radius window: 0.500 <= R <= 2.500 solar radii
Rows after radius window: 212
ROBUST: True
Rows before robust cut: 212
Rows after robust cut: 103
  robust Teff: 5500 <= Teff <= 6800
  robust logg: 3.75 <= logg <= 4.45
  robust L: 1 <= L <= 11
  robust Meta: -0.5 <= Meta <= 0.27
Rows used for final residual-vs-oblateness analysis: 103

Residual definitions:
  delta_R = rad_pred - R
  frac_residual = (rad_pred - R) / R
  sigma_delta_R = sqrt(rad_sigma^2 + sigma_R_true^2)
  z_R = delta_R / sigma_delta_R

delta_R: n=103, mean=-0.035669, median=-0.00343259, std=0.150054, min=-0.619556, max=0.319803
frac_residual: n=103, mean=-0.0156398, median=-0.00255725, std=0.0829338, min=-0.364659, max=0.193937
z_R: n=103, mean=-0.372524, median=-0.0403395, std=1.79018, min=-8.2375, max=3.54914
z_R_q68: n=103, mean=-0.440825, median=-0.0889806, std=1.87621, min=-8.24898, max=3.57874
oblateness: n=103, mean=0.010642, median=0.00276, std=0.019378, min=4.9e-07, max=0.118
fill_factor: n=103, mean=0.281161, median=0.251, std=0.196644, min=0.0141, max=0.875
sigma_pred_q68: n=103, mean=0.0567501, median=0.0400707, std=0.0481715, min=0.00951184, max=0.24255
rad_sigma: n=103, mean=0.547356, median=0.0410922, std=3.24148, min=0.00979528, max=32.1097

68% interval coverage: 0.417
95% interval coverage: 0.699

Most relevant correlations:
                x             y   n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 103  -0.202666   0.040063     -0.271840    0.005474     -0.014349         -0.056051
      fill_factor frac_residual 103  -0.128731   0.194997     -0.273434    0.005196     -0.054292         -0.000375
log10_fill_factor frac_residual 103  -0.203799   0.038940     -0.273434    0.005196     -0.043270         -0.045319

Multivariable regression:
  Responses: frac_residual and abs_frac_residual
  Predictors are standardized before fitting; standard errors are HC3 robust.
  Table: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_14568_radius_residuals\EB_multivariable_regression_HC3.csv

Plot-bin statistics:
  Final plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_14568_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness.csv
  Pre-radius-cut plot bins: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_different_predictions\seed_14568_radius_residuals\EB_plot_binned_residuals_vs_log10_oblateness_before_rad_cut.csv