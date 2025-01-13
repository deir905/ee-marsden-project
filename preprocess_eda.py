import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

# Upsampling from 4 to 64 Hz was necessary for EDA pre-processing. 
# To remove any artifacts, smoothing using the Gaussian low pass filter, with a 40-point window and sigma of 400 ms, is carried out

# Load your CSV file into a DataFrame
df = pd.read_csv('eda.csv')

# Convert Unix timestamps from microseconds to seconds
df['unix_timestamp'] = df['unix_timestamp'] / 1_000_000  # Dividing by 1,000,000 to convert microseconds to seconds

# Assuming your EDA signal is in a column named 'EDA'
time = df['unix_timestamp'].values  # Time in seconds
eda = df['eda'].values    # Original EDA values

# Define new time points for 64 Hz (0.015625 seconds apart)
new_time = np.arange(time[0], time[-1], 1/64)

# Interpolate EDA values at the new time points
interp_func = interp1d(time, eda, kind='linear')
new_eda = interp_func(new_time)

# Apply Gaussian filter with a sigma of 25.6 points (as calculated earlier)
# Convert ms to seconds and multiply by 64 Hz to get the number of points
sigma_points = 400 / 1000 * 64  
smoothed_eda = gaussian_filter1d(new_eda, sigma=sigma_points)

# Save the processed data back to a CSV file
processed_df = pd.DataFrame({'unix_timestamp': new_time, 'eda': smoothed_eda})
processed_df.to_csv('processed_eda.csv', index=False)
