import os
import pandas as pd

base_dir = '../data'

# list of participants
participants = [f'{i:02d}' for i in range(1, 25)]

# list of subfolders to process
subfolders = ['gaze', 'move']

# columns to select from the raw data file
columns_to_select = [
    'PARTICIPANT', 'SESSION', 'BLOCK', 'TRIAL', 'TRIAL_ORDER',
    'CLOSEST_RELEVANT_TIME', 'CLOSEST_RELEVANT_SHOWN', 'CLOSEST_IRRELEVANT_TIME', 
    'CLOSEST_IRRELEVANT_SHOWN', 'TRIAL_TIME', 'TRIAL_CLOSEST_RELEVANT_TIME', 
    'TRIAL_CLOSEST_IRRELEVANT_TIME'
]

# iterate through each participant folder
for participant in participants:
    participant_dir = os.path.join(base_dir, participant)
    
    for subfolder in subfolders:
        dir_path = os.path.join(participant_dir, subfolder, 'gaze_blocks')
        
        if not os.path.exists(dir_path):
            continue
        
        # list all files in the gaze_blocks folder
        files = os.listdir(dir_path)
        
        # filter for _events.csv files
        events_files = [f for f in files if f.endswith('_events.csv')]
        
        for events_file in events_files:
            # corresponding raw data file
            raw_data_file = events_file.replace('_events.csv', '.csv')
            
            events_path = os.path.join(dir_path, events_file)
            raw_data_path = os.path.join(dir_path, raw_data_file)
            
            if not os.path.exists(raw_data_path):
                print(f"Raw data file {raw_data_path} does not exist.")
                continue
            
            events_df = pd.read_csv(events_path)
            raw_data_df = pd.read_csv(raw_data_path)
            raw_data_df["TRIAL_TIME"] = raw_data_df["TRIAL_TIME"].round(decimals=2)
            
            # select columns from raw_data_df
            raw_data_df_subset = raw_data_df[columns_to_select]
            
            # merge dataframes based on 'TRIAL_TIME' in raw_data_df and 'onset' in events_df
            merged_df = pd.merge(events_df, raw_data_df_subset, left_on='onset', right_on='TRIAL_TIME', how='left', suffixes=('_event', '_raw'))
            
            # drop the duplicate TRIAL_TIME column
            #merged_df.drop(columns=['TRIAL_TIME'], inplace=True)
            
            # save to new CSV
            output_filename = events_file.replace('_events.csv', '_merged.csv')
            output_path = os.path.join(dir_path, output_filename)
            merged_df.to_csv(output_path, index=False)
            
            print(f"Merged file created: {output_path}")
            
            assert len(events_df) == len(merged_df)

print("Data processing completed.")