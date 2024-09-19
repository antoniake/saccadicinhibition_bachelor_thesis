import pandas as pd
import os
from src import helper as hlp # get_viewing_distance, scaling_func
from src import csv_converter as cc # convert_tsv

file_path = '../data'

# Loop through each participant folder from '01' to '24'
for i in range(1, 25):
    participant_folder = f'{file_path}/{str(i).zfill(2)}'
    
    # Loop through each of the subfolders 'gaze' and 'move'
    for subfolder_name in ['gaze', 'move']:
        subfolder = f'{participant_folder}/{subfolder_name}/gaze_blocks'
        
        if os.path.exists(subfolder):
            files = os.listdir(subfolder)
            
            for file_name in files:
                if file_name.startswith('split_data_SESSION') and file_name.endswith('.csv') and 'event' not in file_name:
                    try:
                        file = f'{subfolder}/{file_name}'
                        df = pd.read_csv(file, escapechar='\n')
                        #print(df.head()['VIEWING_DISTANCE'])
                        
                        # Calculate viewing distance and scaling factor
                        viewing_distance = hlp.get_viewing_distance(df)
                        #print(viewing_distance)
                        scaling_factor = hlp.scaling_func(viewing_distance)  # Default screen_size and resolution
                        #print(scaling_factor)
                        
                        # Convert TSV
                        file_conv = cc.convert_tsv(file)
                        file_target = f'{subfolder}/{file_name.replace(".csv", "_events.tsv")}'
                        
                        # Run remodnav command with scaling factor
                        os.system(f"remodnav {file_conv} {file_target} {scaling_factor} 50 --savgol-length 0.06 --min-saccade-duration 0.02 --noise-factor 3")
                        
                        print(f'Processed file: {file}')
                        
                        # Convert TSV to CSV
                        tsv_file_path = file_target
                        csv_file_path = f'{subfolder}/{file_name.replace(".csv", "_events.csv")}'
                        df_tsv = pd.read_csv(tsv_file_path, sep='\t')
                        df_tsv.to_csv(csv_file_path, index=False)
                        
                        print(f'Converted TSV to CSV: {csv_file_path}')

                    except FileNotFoundError:
                        print(f'File not found: {file}')

                    except Exception as e:
                        #raise e
                        print(f'An error occurred while processing {file}: {e}')