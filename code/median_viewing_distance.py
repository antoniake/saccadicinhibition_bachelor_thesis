import os
import pandas as pd

# Define the path to the parent directory containing all participant folders
parent_dir = '../data'

# Initialize a dictionary to store the median viewing distance for each participant
median_viewing_distances = {}

# Loop through each participant's folder
for participant in os.listdir(parent_dir):
    participant_path = os.path.join(parent_dir, participant)
    
    # Check if it's a directory
    if os.path.isdir(participant_path):
        viewing_distances = []
        
        for i in range(1, 25):
            if i in {5, 7, 20, 21}:  # Skip the missing numbers
                continue
            
            # Construct file paths
            gaze_path = os.path.join(participant_path, 'gaze', f'gaze_data_{i:02d}_gaze.csv')
            move_path = os.path.join(participant_path, 'move', f'gaze_data_{i:02d}_move.csv')
            
            # Check if files exist
            if os.path.exists(gaze_path):
                # Read the CSV file
                gaze_data = pd.read_csv(gaze_path)
                # Extract the 'VIEWING_DISTANCE' column
                viewing_distances.extend(gaze_data['VIEWING_DISTANCE'].tolist())
            
            if os.path.exists(move_path):
                # Read the CSV file
                move_data = pd.read_csv(move_path)
                # Extract the 'VIEWING_DISTANCE' column
                viewing_distances.extend(move_data['VIEWING_DISTANCE'].tolist())
        
        # Calculate the median viewing distance if any data was collected
        if viewing_distances:
            median_distance = pd.Series(viewing_distances).median()
            median_viewing_distances[participant] = median_distance

# Convert the dictionary to a DataFrame for better visualization
median_viewing_distances_df = pd.DataFrame.from_dict(median_viewing_distances, orient='index', columns=['Median Viewing Distance'])

# Display the dataframe using standard pandas functionality
median_viewing_distances_df.to_csv('../results/median_viewing_distance_all.csv')
