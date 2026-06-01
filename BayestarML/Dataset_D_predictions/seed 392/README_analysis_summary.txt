Input file: Dataset_D_predictions\EB_oblateness_fill_factor_mass_predictions_4_features_3000_draws_seed_392.csv
Input rows: 295
Rows usable before mass cut: 295
Pre-mass-cut plots directory: C:\Users\ngeorgakopulos\Desktop\Metalurgia\tests\code\BayeStarML\BayestarML\Dataset_D_predictions\seed 392\plots_before_mass_cut
Mass window: 0.950 <= M <= 1.500 solar masses
Rows after mass window: 138
ROBUST: True
Rows before robust cut: 138
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

delta_M: n=85, mean=-0.0149593, median=-0.000618813, std=0.126309, min=-0.444363, max=0.450802
frac_residual: n=85, mean=-0.00816058, median=-0.000512262, std=0.104869, min=-0.299033, max=0.439807
z_M: n=85, mean=-0.2898, median=-0.00269222, std=2.10469, min=-6.7724, max=4.90844
z_M_q68: n=85, mean=-0.453489, median=-0.0232476, std=2.75134, min=-9.20486, max=7.87975
oblateness: n=85, mean=0.00983378, median=0.002431, std=0.0188387, min=4.9e-07, max=0.118
fill_factor: n=85, mean=0.271823, median=0.2386, std=0.192285, min=0.0141, max=0.875
sigma_pred_q68: n=85, mean=0.0449306, median=0.0393251, std=0.0216359, min=0.0139569, max=0.116732
mass_sigma: n=85, mean=0.425971, median=0.0554067, std=1.2359, min=0.0154004, max=6.87194

68% interval coverage: 0.353
95% interval coverage: 0.694

Most relevant correlations:
                x             y  n  pearson_r  pearson_p  spearman_rho  spearman_p  linear_slope  linear_intercept
 log10_oblateness frac_residual 85  -0.045716   0.677809     -0.107505    0.327425     -0.004025         -0.019705
      fill_factor frac_residual 85   0.051975   0.636635     -0.106226    0.333247      0.028346         -0.015866
log10_fill_factor frac_residual 85  -0.046874   0.670113     -0.106226    0.333247     -0.012379         -0.016865