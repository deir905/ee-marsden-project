import heartpy as hp
import matplotlib.pyplot as plt
import os
import argparse
import csv
from datetime import datetime
from avro_to_csv import convert_avro_to_csv

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


def analysePulseRate(output_dir):
    # Load .csv file
    input_file = os.path.join(output_dir, 'bvp.csv')
    bvp_data = hp.get_data(input_file, column_name = 'bvp')
    timer_data = hp.get_data(input_file, column_name='unix_timestamp')
    
    # Datetime requires timestamp in seconds
    # Convert unix_timestamp from microseconds to seconds
    timer_data = timer_data/1000000
    # Convert each timestamp to a formatted datetime object
    datetime_data = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f') for ts in timer_data]
    # Calculate sample rate
    sample_rate = int(hp.get_samplerate_datetime(datetime_data, timeformat='%Y-%m-%d %H:%M:%S.%f'))
    print('sample rate is: %f Hz' %sample_rate)
    
    # Get user input for timestamp windows
    user_timestamps = get_user_timestamps(datetime_data)
    # Find indices for the given timestamp windows
    indices = find_indices_for_timestamps(datetime_data, user_timestamps)
    print(indices)

    # Analyse each period
    for idx, (start_index, end_index) in enumerate(indices):
        filtered_ppg = hp.filter_signal(bvp_data[start_index: end_index], 
                                cutoff = [0.8, 2.5], 
                                filtertype = 'bandpass',
                                sample_rate = sample_rate, 
                                order = 3,
                                return_top = False)
        
        wd, m = hp.process(filtered_ppg, sample_rate=sample_rate,
                   high_precision = True, clean_rr = True)

        plot_object = hp.plotter(wd, m, title='Heart Beat Detection from: ' + user_timestamps[idx][0] + ' to ' + user_timestamps[idx][1], show=False)
        plot_object.savefig(output_dir + '/hr_plot_' + str(idx) + '.jpg') 
        plot_object.show()
        
        for key in m.keys():
            print('%s: %f' %(key, m[key]))

        with open(os.path.join(output_dir, 'pulse_rate_analysis.csv'), 'a', newline='') as f:
            writer = csv.writer(f)
            # Only write the header if the file is being created, not when appending.
            if f.tell() == 0:
                writer.writerow(["start", "end"] + list(m.keys()))  
             # Write the row with start_index, end_index, and the values from m
            writer.writerow([user_timestamps[idx][0], user_timestamps[idx][1]] + [m[key] for key in m.keys()])




if __name__=="__main__":
        # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert an Avro file to CSV files for each sensor data type.")
    parser.add_argument("input_file", help="Path to the input Avro file.")
    args = parser.parse_args()
    # Get the Avro file path from the command-line argument
    avro_file_path = args.input_file
    output_dir = convert_avro_to_csv(avro_file_path)
    
    analysePulseRate(output_dir)