import os
import re
import pandas as pd

# Path to the main directory
main_dir = '../data'

# Function to extract numerical values from filename
def extract_numbers(filename):
    match = re.search(r'SESSION_(\d+.\d+)_BLOCK_(\d+.\d+)_TRIAL_ORDER_(\d+.\d+)_merged', filename)
    if match:
        session = float(match.group(1))
        block = float(match.group(2))
        trial_order = float(match.group(3))
        return session, block, trial_order
    else:
        return None

# Function to get sorted file paths
def get_sorted_file_paths(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('_merged.csv')]
    sorted_files = sorted(files, key=lambda x: extract_numbers(x))
    file_paths = [os.path.join(folder_path, f) for f in sorted_files]
    return file_paths

# Function to process and concatenate CSV files
def concatenate_csv_files(participant_id, subfolder):
    folder_path = f'{main_dir}/{str(participant_id).zfill(2)}/{subfolder}/gaze_blocks'
    file_paths = get_sorted_file_paths(folder_path)
    
    if not file_paths:  # Check if there are no files to process
       print(f"No files found for participant {participant_id} in {subfolder} subfolder.")
       return
    
    dfs = [pd.read_csv(file_path) for file_path in file_paths]
    concatenated_df = pd.concat(dfs, ignore_index=True)
    
    output_path = f'{main_dir}/participant_{str(participant_id).zfill(2)}_{subfolder}_concat.csv'
    concatenated_df.to_csv(output_path, index=False)

# Iterate through participant folders
for participant_id in range(1, 25):
    participant_folder = f'{main_dir}/{str(participant_id).zfill(2)}'
    if not os.path.exists(participant_folder):
        print(f"Participant folder {participant_folder} does not exist.")
        continue
    
    for subfolder in ['gaze', 'move']:
        subfolder_path = f'{participant_folder}/{subfolder}'
        if not os.path.exists(subfolder_path):
            print(f"Subfolder {subfolder_path} does not exist for participant {participant_id}.")
            continue
        
        concatenate_csv_files(participant_id, subfolder)

print("Concatenation completed for all participants.")