import pandas as pd
import pingouin 

file_path = '../results/df_hypothesis2.csv'
df = pd.read_csv(file_path)

mean_mean_stimtype = df.groupby(['stimulus type'])['mean'].agg(['mean', 'std']).reset_index()
mean_mean_condition = df.groupby(['condition'])['mean'].agg(['mean', 'std']).reset_index()
mean_mean_both = df.groupby(['condition', 'stimulus type'])['mean'].agg(['mean', 'std']).reset_index()

pd.set_option('display.max_columns', None)
print(mean_mean_stimtype)
#  stimulus type      mean       std
#0      baseline  3.482808  0.707180
#1    irrelevant  3.564411  0.736175
#2      relevant  3.526410  0.811938

print(mean_mean_condition)
#  condition      mean       std
#0      gaze  3.728573  0.726128
#1      move  3.320514  0.717579

# dataframe with gaze and move values
gaze_values = df[df['condition'] == 'gaze']['mean'].reset_index(drop=True)
move_values = df[df['condition'] == 'move']['mean'].reset_index(drop=True)

df_ttest_hyp2 = pd.DataFrame({
    'gaze': gaze_values,
    'move': move_values
})

print(df_ttest_hyp2)

# paired ttest: gaze vs. move 

result_hyp2 = pingouin.ttest(x = df_ttest_hyp2['gaze'],
               y = df_ttest_hyp2['move'],
               paired = True,
               alternative = 'two-sided')
pd.set_option('display.max_columns', None)
print(result_hyp2)

# p = 8.447416e-09
## mit 300 move trials: p = 0.000012

result2_hyp2 = pingouin.ttest(x = df_ttest_hyp2['move'],
               y = df_ttest_hyp2['gaze'],
               paired = True,
               alternative = 'less')
pd.set_option('display.max_columns', None)
print(result2_hyp2)

# p = 4.223708e-09
## mit 300 move trials: p = 0.000006

# lower saccadic frequency in move condition -> literature, smoother eye movements
# in combined gaze-hands tasks