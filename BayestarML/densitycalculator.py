import pandas as pd
import numpy as np

# 1. Read your .txt file (assuming it's tab-separated)
df = pd.read_csv('Datasets/data_sample_mass_radius.txt', sep='\t')

# 2. Calculate density (rho)
df['rho'] = (3 * df['M']) / (4 * np.pi * df['R']**3)

# 3. Calculate propagated errors (erho1 and erho2)
df['erho1'] = df['rho'] * np.sqrt((df['eM1'] / df['M'])**2 + 9 * (df['eR1'] / df['R'])**2)
df['erho2'] = df['rho'] * np.sqrt((df['eM2'] / df['M'])**2 + 9 * (df['eR2'] / df['R'])**2)

# 4. Save the updated data back to a new .txt file
df.to_csv('Datasets/data_sample_calculated_density.txt', sep='\t', index=False)

print("Data processing complete!")