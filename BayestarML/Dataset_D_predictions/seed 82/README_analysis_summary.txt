Input file: Dataset_D_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_82.csv
Input rows: 297
Rows usable before mass cut: 297
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed 82\plots_before_mass_cut
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

delta_M: n=85, mean=-0.0152114, median=-0.0131694, std=0.125731, min=-0.445316, max=0.442361
frac_residual: n=85, mean=-0.00850158, median=-0.0110044, std=0.104329, min=-0.299674, max=0.431572
z_M: n=85, mean=-0.286741, median=-0.00339061, std=2.00569, min=-6.60899, max=4.48447
z_M_q68: n=85, mean=-0.44545, median=-0.159075, std=2.65348, min=-9.07213, max=7.40761
oblateness: n=85, mean=0.00983378, median=0.002431, std=0.0188387, min=4.9e-07, max=0.118
fill_factor: n=85, mean=0.271823, median=0.2386, std=0.192285, min=0.0141, max=0.875
sigma_pred_q68: n=85, mean=0.046631, median=0.0407047, std=0.0220305, min=0.0143981, max=0.119769
mass_sigma: n=85, mean=0.450205, median=0.0569563, std=1.35044, min=0.0158398, max=8.19746

68% interval coverage: 0.353
95% interval coverage: 0.706

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 85  -0.050680   0.645070     -0.117130    0.285713     -0.004439         -0.021234
      fill_factor frac_residual 85   0.045362   0.680169     -0.115831    0.291124      0.024612         -0.015192
log10_fill_factor frac_residual 85  -0.051830   0.637574     -0.115831    0.291124     -0.013617         -0.018077