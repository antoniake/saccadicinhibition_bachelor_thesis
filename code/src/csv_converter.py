import pandas as pd
import os

def convert_tsv(filename):
    filename=filename
    file = pd.read_csv(f'{filename}',escapechar='\n')
    file = file[['X_POS_SCREEN','Y_POS_SCREEN']]
    new_filename = filename.split(".csv")[0]
    file.to_csv(f'{new_filename}.tsv', sep='\t', header=None, encoding=None, index=False)
    
    return os.path.abspath(f'{new_filename}.tsv')
