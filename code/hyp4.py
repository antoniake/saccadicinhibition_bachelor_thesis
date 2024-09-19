# Hypothesis 4: compare peaks

import pandas as pd
import pingouin as pg

file_path = '../results/df_hypothesis3and4.csv'
df_anova = pd.read_csv(file_path)

#descriptives
mean_max_normrate = df_anova.groupby(['condition','stimulus type'])['normalised max rate'].agg(['mean', 'std']).reset_index()
mean_peakmagnitude = df_anova.groupby(['condition','stimulus type'])['peak magnitude'].agg(['mean', 'std']).reset_index()
mean_latpeak = df_anova.groupby(['condition','stimulus type'])['latency peak'].agg(['mean', 'std']).reset_index()

pd.set_option('display.max_columns', None)
print(mean_max_normrate)
#  condition stimulus type      mean       std
#0      gaze    irrelevant  1.287954  0.255992
#1      gaze      relevant  1.878004  0.381748
#2      move    irrelevant  1.382433  0.324858 #TODO
#3      move      relevant  1.850197  0.413934
print(mean_peakmagnitude)
#  condition stimulus type      mean       std
#0      gaze    irrelevant  0.287954  0.255992
#1      gaze      relevant  0.878004  0.381748
#2      move    irrelevant  0.382433  0.324858 #TODO
#3      move      relevant  0.850197  0.413934
print(mean_latpeak)
#  condition stimulus type    mean        std
#0      gaze    irrelevant  158.60  37.553330
#1      gaze      relevant  179.00  21.479488
#2      move    irrelevant  168.10  47.987827 #TODO
#3      move      relevant  170.35  29.519441

anova_peak = pg.rm_anova(data=df_anova, dv='peak magnitude', 
                  within=['condition', 'stimulus type'], 
                  subject='participant')
pd.set_option('display.max_columns', None)
print(anova_peak)

# condition:                 F = 0.381331    p = 0.5442224      n2 = 0.002391
# stimulus type:             F = 121.339068  p = 1.084469e-09   n2 = 0.376265
# condition * stimulus type: F = 3.372231    p = 0.08200194     n2 = 0.007997

#post hoc
post_hoc = pg.pairwise_tests(dv='peak magnitude', 
                             within=['condition', 'stimulus type'], 
                             subject='participant', 
                             data=df_anova, 
                             padjust='bonf')

print(post_hoc)
# condition         -                  gaze        move     T =  -0.617520, p = 0.5442224 (not significant, first group lower)
# stimulus type         -              irrelevant  relevant T = -11.015401, p = 1.084469e-09 (first group lower)
# condition * stimulus type      gaze  irrelevant  relevant T = -11.704905, p = 3.940709e-10, bonf 7.881417e-10 (first group lower) 
# condition * stimulus type      move  irrelevant  relevant T =  -7.144224, p = 8.620461e-07, bonf 1.724092e-06 (first group lower)