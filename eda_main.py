import heartpy as hp
import matplotlib.pyplot as plt
import neurokit2 as nk
import os
import argparse
import csv
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from datetime import datetime
from avro_to_csv import convert_avro_to_csv

plt.rcParams['figure.figsize'] = [15, 5] 
PERIOD_COUNT = 3

def get_user_timestamps(datetime_data):
    periods = PERIOD_COUNT
    timestamps = []
    print("Please enter the start and end timestamps for each period in the format %Y-%m-%d %H:%M:%S.")
    print("Minimum timestamp of recording is: " + datetime_data[0])
    print("Maximum timestamp of recording is: " + datetime_data[-1])
    for i in range(periods):
        start = input(f"Period {i+1} start: ")
        end = input(f"Period {i+1} end: ")
        timestamps.append((start, end))
    return timestamps


def find_indices_for_timestamps(datetime_data, user_timestamps):
    indices = []
    datetime_objs = [datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f') for dt in datetime_data]
    
    for start, end in user_timestamps:
        start_obj = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_obj = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        
        start_index = next(i for i, dt in enumerate(datetime_objs) if dt > start_obj)
        end_index = next(i for i, dt in enumerate(datetime_objs) if dt > end_obj)
        
        indices.append((start_index, end_index))
    
    return indices

def preprocess_eda(input_file):
    # Load your CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
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
    
    processed_df = pd.DataFrame({'unix_timestamp': new_time, 'eda': smoothed_eda})
    return processed_df

def analyseEDA(output_dir):
    # Load .csv file
    input_file = os.path.join(output_dir, 'eda.csv')
    processed_eda = preprocess_eda(input_file)
    eda_data = processed_eda['eda']
    timer_data = processed_eda['unix_timestamp']
    
    # Datetime requires timestamp in seconds
    # Convert each timestamp to a formatted datetime object
    datetime_data = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f') for ts in timer_data]
    # Calculate sample rate
    sample_rate = int(hp.get_samplerate_datetime(datetime_data, timeformat='%Y-%m-%d %H:%M:%S.%f'))
    print('sample rate is: %f Hz' %sample_rate)

    #plot data
    plt.figure(figsize=(12,6))
    plt.plot(eda_data)
    plt.show() 

    
    # Get user input for timestamp windows
    user_timestamps = get_user_timestamps(datetime_data)
    # Find indices for the given timestamp windows
    indices = find_indices_for_timestamps(datetime_data, user_timestamps)
    print(indices)

    # Analyse each period
    for idx, (start_index, end_index) in enumerate(indices):
        print( eda_data[start_index:end_index])
        # Process the EDA signal
        signals, info = nk.eda_process(eda_data[start_index: end_index], sampling_rate=sample_rate)
        print( eda_data[start_index:end_index])

        # Filter phasic and tonic components
        data = nk.eda_phasic(nk.standardize(eda_data[start_index:end_index]), sampling_rate=sample_rate)
        print( eda_data[start_index:end_index])

        data['EDA_Raw'] = eda_data[start_index:end_index].values  # Add raw signal
        data.plot()
        print(data)

        # Plot EDA signal
        nk.eda_plot(signals, info)
        # plot_object = nk.eda_plot(signals, info)
        # plot_object.savefig(output_dir + '/eda_plot_' + str(idx) + '.jpg') 
        # plot_object.show()



        with open(os.path.join(output_dir, 'eda_analysis.csv'), 'a', newline='') as f:
            writer = csv.writer(f)
            # Only write the header if the file is being created, not when appending.
            if f.tell() == 0:
                writer.writerow(["start", "end", "EDA_Tonic_Mean", "Raw_EDA_Mean"])  
             # Write the row with start_index, end_index, and the values from m
            writer.writerow([user_timestamps[idx][0], user_timestamps[idx][1], data['EDA_Tonic'].mean(), data['EDA_Raw'].mean()])




if __name__=="__main__":
        # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert an Avro file to CSV files for each sensor data type.")
    parser.add_argument("input_file", help="Path to the input Avro file.")
    args = parser.parse_args()
    # Get the Avro file path from the command-line argument
    avro_file_path = args.input_file
    output_dir = convert_avro_to_csv(avro_file_path)
    
    analyseEDA(output_dir)