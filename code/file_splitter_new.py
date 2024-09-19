import numpy as np
import pandas as pd
import os

def repeated_file_splits(path, out_folder_name, split_columns, file_prefix, normalize_columns, normalize_by, normalize_prefix):
    # Loop through each participant folder from '01' to '24'
    for i in range(1, 25):
        participant_folder = f'{path}/{str(i).zfill(2)}'
        
        for subfolder_name in ['gaze', 'move']:
            subfolder = f'{participant_folder}/{subfolder_name}'
            filename = f'gaze_data_{str(i).zfill(2)}_{subfolder_name}.csv'
            
            if os.path.exists(subfolder) and filename in os.listdir(subfolder):
                in_path = os.path.join(subfolder, filename)
                out_path = os.path.join(subfolder, out_folder_name)
                
                # Ensure the output directory exists
                if not os.path.isdir(out_path):
                    os.makedirs(out_path)
                
                # Run the file splitting function
                file_splitter(in_path, out_path, split_columns, file_prefix, normalize_columns, normalize_by, normalize_prefix)

def file_splitter(filepath, out_folder, split_columns, prefix, normalize_columns, normalize_by, normalize_prefix):
    # Read data
    data = pd.read_csv(filepath)
    # Get the unique value combinations we want to filter for
    unique_tuples = get_unique_tuples(data, split_columns)
    # Filter the data
    for combination in unique_tuples:
        comb_data = data
        file_name = ''
        for name, val in zip(split_columns, combination):
            comb_data = comb_data[comb_data[name] == val]
            file_name = file_name+f'_{name}_{val}'
        # Save as new file
        for normalize_col in normalize_columns:
            comb_data[f'{normalize_prefix}_{normalize_col}'] = comb_data[normalize_col] - comb_data[normalize_by].iloc[0]
        comb_data.to_csv(f'{out_folder}/{prefix}{file_name}.csv', index=False)

def get_unique_tuples(data, columns):
    column_data = data[columns].dropna(axis=0)
    unique_tuples = np.unique(column_data.values, axis=0)
    return unique_tuples

# Use example - you can run this program in your console as file_splitter.py (don't forget to change the path)
# or import to python and copy the code below.
if __name__ == "__main__":
    path = '../data'
    out_folder = 'gaze_blocks'
    split_columns = ['SESSION', 'BLOCK', 'TRIAL_ORDER']
    file_prefix = 'split_data'
    normalize_columns = ['TIME', 'CLOSEST_RELEVANT_TIME', 'CLOSEST_IRRELEVANT_TIME']
    normalize_prefix = 'TRIAL'
    normalize_by = 'TIME'
 
    repeated_file_splits(path, out_folder, split_columns, file_prefix, normalize_columns, normalize_by, normalize_prefix)
