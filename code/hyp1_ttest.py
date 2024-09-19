import pandas as pd
import pingouin 

file_path = '../results/df_hypothesis1.csv'
df = pd.read_csv(file_path)

# mean of minimum of saccade rate per stimulus per condition

mean_minimum_stimtype = df.groupby(['stimulus type'])['minimum'].agg(['mean', 'std']).reset_index()
mean_minimum_condition = df.groupby(['condition'])['minimum'].agg(['mean', 'std']).reset_index()
mean_minimum_both = df.groupby(['condition', 'stimulus type'])['minimum'].agg(['mean', 'std']).reset_index()

pd.set_option('display.max_columns', None)
print(mean_minimum_both)

#  condition stimulus type      mean       std
#0      gaze      baseline  3.294880  0.673240
#1      gaze    irrelevant  2.563012  0.693542
#2      gaze      relevant  2.961056  0.593000
#3      move      baseline  2.824036  0.660723
#4      move    irrelevant  2.489728  0.657417
#5      move      relevant  2.376999  0.649064

pd.set_option('display.max_columns', None)
print(mean_minimum_condition)

#  condition      mean       std
#0      gaze  2.939649  0.710719
#1      move  2.563587  0.672369

pd.set_option('display.max_columns', None)
print(mean_minimum_stimtype)

#  stimulus type      mean       std
#0      baseline  3.059458  0.700243
#1    irrelevant  2.526370  0.668033
#2      relevant  2.669027  0.681194

# split into gaze and move dataframes
df_gaze = df[df['condition'] == 'gaze']
df_move = df[df['condition'] == 'move']

# restructure the dataframe
df_gaze_ttest = df_gaze.pivot_table(index='participant', columns='stimulus type', 
                         values='minimum', aggfunc='mean').reset_index()
#print(df_gaze_ttest)

df_move_ttest = df_move.pivot_table(index='participant', columns='stimulus type', 
                         values='minimum', aggfunc='mean').reset_index()

# Rename columns to match the desired format
df_gaze_ttest.columns.name = None  # Remove the index name
df_gaze_ttest = df_gaze_ttest.rename(columns={'irrelevant': 'irrelevant', 
                                  'relevant': 'relevant', 'baseline': 'baseline'})
#print(df_gaze_ttest) 

df_move_ttest.columns.name = None  # Remove the index name
df_move_ttest = df_move_ttest.rename(columns={'irrelevant': 'irrelevant', 
                                  'relevant': 'relevant', 'baseline': 'baseline'})
#print(df_move_ttest) 

# GAZE paired t-test: baseline vs. relevant
result_rel_g = pingouin.ttest(x = df_gaze_ttest['relevant'],
               y = df_gaze_ttest['baseline'],
               paired = True,
               alternative = 'less')
pd.set_option('display.max_columns', None)
print(result_rel_g)

## p = 0.000293

# GAZE paired t-test: baseline vs. irrelevant
result_irrel_g = pingouin.ttest(x = df_gaze_ttest['irrelevant'],
               y = df_gaze_ttest['baseline'],
               paired = True,
               alternative = 'less')
pd.set_option('display.max_columns', None)
print(result_irrel_g)

## p = 9.041880e-08

# MOVE paired t-test: baseline vs. relevant
result_rel_m = pingouin.ttest(x = df_move_ttest['relevant'],
               y = df_move_ttest['baseline'],
               paired = True,
               alternative = 'less')
pd.set_option('display.max_columns', None)
print(result_rel_m)

## p = 0.000021
## mit 300 trials: p = 0.001116

# MOVE paired t-test: baseline vs. irrelevant
result_irrel_m = pingouin.ttest(x = df_move_ttest['irrelevant'],
               y = df_move_ttest['baseline'],
               paired = True,
               alternative = 'less')
pd.set_option('display.max_columns', None)
print(result_irrel_m)

## p = 0.000046
## mit 300 trials: p = 0.002877