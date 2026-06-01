Input file: Dataset_D_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_29.csv
Input rows: 297
Rows usable before mass cut: 297
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed 29\plots_before_mass_cut
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

delta_M: n=85, mean=-0.0150896, median=-0.0141351, std=0.125271, min=-0.444681, max=0.459961
frac_residual: n=85, mean=-0.00845516, median=-0.0113081, std=0.104092, min=-0.299247, max=0.448742
z_M: n=85, mean=-0.268622, median=-0.00658124, std=2.03072, min=-6.54707, max=4.18328
z_M_q68: n=85, mean=-0.412113, median=-0.145364, std=2.72025, min=-9.02955, max=8.05155
oblateness: n=85, mean=0.00983378, median=0.002431, std=0.0188387, min=4.9e-07, max=0.118
fill_factor: n=85, mean=0.271823, median=0.2386, std=0.192285, min=0.0141, max=0.875
sigma_pred_q68: n=85, mean=0.0461663, median=0.0382808, std=0.0233314, min=0.0140442, max=0.12466
mass_sigma: n=85, mean=0.393848, median=0.0592292, std=1.17926, min=0.0153149, max=8.61223

68% interval coverage: 0.353
95% interval coverage: 0.694

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 85  -0.033222   0.762773     -0.096795    0.378172     -0.002904         -0.016782
      fill_factor frac_residual 85   0.061405   0.576660     -0.095516    0.384536      0.033241         -0.017491
log10_fill_factor frac_residual 85  -0.034246   0.755685     -0.095516    0.384536     -0.008977         -0.014768