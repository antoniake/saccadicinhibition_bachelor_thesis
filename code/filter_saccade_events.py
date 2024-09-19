import os
import pandas as pd

# Path to the main directory
main_dir = '../data'

# Function to filter rows and create new CSV files
def create_saccades_files():
    for participant_id in range(1, 25):
        participant_id_str = str(participant_id).zfill(2)
        for subfolder in ['gaze', 'move']:
            input_file = f'{main_dir}/participant_{participant_id_str}_{subfolder}_concat.csv'
            output_file = f'{main_dir}/participant_{participant_id_str}_{subfolder}_saccades.csv'
            
            if os.path.exists(input_file):
                df = pd.read_csv(input_file)
                
                # Filter rows where label is "ISAC" or "SACC"
                filtered_df = df[df['label'].isin(['ISAC', 'SACC'])]
                
                # Save the filtered dataframe to the new file
                filtered_df.to_csv(output_file, index=False)
                print(f"Created {output_file}")
            else:
                print(f"File {input_file} does not exist.")

if __name__ == "__main__":
    create_saccades_files()

print("Saccades files created for all participants.")