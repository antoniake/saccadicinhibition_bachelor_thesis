import pandas as pd
import pingouin 

file_path = '../results/df_hypothesis3.csv'
df = pd.read_csv(file_path)

mean_normrate = df.groupby(['condition','stimulus type'])['normalised min rate'].agg(['mean', 'std']).reset_index()
mean_maxinhib = df.groupby(['condition','stimulus type'])['magnitude of max inhibition'].agg(['mean', 'std']).reset_index()
mean_latmaxinhib = df.groupby(['condition','stimulus type'])['latency max inhibition'].agg(['mean', 'std']).reset_index()

pd.set_option('display.max_columns', None)
print(mean_normrate)
#  condition stimulus type      mean       std
#0      gaze    irrelevant  0.655223  0.162418
#1      gaze      relevant  0.781366  0.175517
#2      move    irrelevant  0.707713  0.177267
#3      move      relevant  0.715533  0.206994

print(mean_maxinhib)
#  condition stimulus type      mean       std
#0      gaze    irrelevant  0.344777  0.162418
#1      gaze      relevant  0.218634  0.175517
#2      move    irrelevant  0.292287  0.177267
#3      move      relevant  0.284467  0.206994

print(mean_latmaxinhib)
#  condition stimulus type   mean        std
#0      gaze    irrelevant  64.60  16.145392
#1      gaze      relevant  53.80  33.372854
#2      move    irrelevant  60.45  14.464021
#3      move      relevant  66.35  29.315480

# magnitude of max inhibition
anova_result = pingouin.rm_anova(data=df, dv='magnitude of max inhibition', 
                  within=['condition', 'stimulus type'], 
                  subject='participant')
pd.set_option('display.max_columns', None)
print(anova_result)

# condition: p = 0.327661
# stimulus type: p = 0.031786
# condition * stimulus type: p = 0.022637
# komplexere aufgaben (mit Handbewebung) führen zu weniger starker inhibition

post_hoc = pingouin.pairwise_tests(dv='magnitude of max inhibition', 
                             within=['condition', 'stimulus type'], 
                             subject='participant', 
                             data=df, 
                             padjust='bonf')
print(post_hoc)

# condition         -                  gaze      move       T = -1.004711, p = 0.327661 (first group lower)
# stimulus type         -              irrelevant  relevant T = 2.317563, p = 0.031786 (first group higher)
# condition * stimulus type      gaze  irrelevant  relevant T = 3.113839, p = 0.005716 (first group higher)
# condition * stimulus type      move  irrelevant  relevant T = 0.223154, p = 0.825797 ( first group higher)

# Condition: There is no significant main effect of condition on the magnitude of max inhibition.
# Stimulus Type: The type of stimulus significantly affects the magnitude of max inhibition, particularly 
#between 'irrelevant' and 'relevant' stimuli.
# Interaction: The effect of stimulus type on inhibition differs depending on whether the participant 
#is in the 'gaze' or 'move' condition, with a significant difference between 'irrelevant' and 'relevant' 
#stimuli within the 'gaze' condition, but not within the 'move' condition.

# latency
anova_result_lat = pingouin.rm_anova(data=df, dv='latency max inhibition', 
                  within=['condition', 'stimulus type'], 
                  subject='participant')
pd.set_option('display.max_columns', None)
print(anova_result_lat)

# condition: p = 0.195864
# stimulus type: p = 0.315985
# condition * stimulus type = 0.155386