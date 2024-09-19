import pandas as pd
import pingouin

file_path = '../results/df_hypothesis3.csv'
df = pd.read_csv(file_path)


# post hoc 

post_hoc_result = pingouin.pairwise_tests(
    dv='normalized minimum rate',
    within=['condition','stimulus type'],
    subject='participant',
    data=df,
    padjust='bonferroni'  # Adjust for multiple comparisons
)

pd.set_option('display.max_columns', None)
print(post_hoc_result)

# bestätigt dass der niedrigste punkt der inhibition nach einem irrelevanten
# reiz niedriger ist als nach relevanten reizen
# und dass interaktion zwischen stimulus type und condition 
# innerhalb von move (rote punkte auf einer linie) kein einfluss von stimulus type
# aber innerhlab von gaze schon
# wenn hand dazu kommt geht effekt der aufgabenrelevanz des reizes verloren

# condition: p = 0.095866 
## comparison between the gaze and move conditions is not statistically 
## significant

# stimulus type: p = 0.000789
## comparison between irrelevant and relevant stimulus types is 
## statistically significant

# condition * stimulus type (gaze): p = 0.000169 (unkorrigiert)
## interaction between condition and stimulus type for the gaze 
## condition is statistically significant

# condition * stimulus tyoe (move): p = 0.123051
## interaction between condition and stimulus type for the move 
## condition is not statistically significant

# Condition: No significant difference between gaze and move condition
# Stimulus Type: Significant difference between irrelevant and relevant 
#                stimuli, with relevant stimuli having a significant 
#                impact on the minimum saccadic rate
# Interaction:
## gaze: there is a significant difference between irrelevant and relevant stimuli
## move: there is no significant difference between irrelevant and relevant stimuli

# while there is no evidence that condition alone affect the minimum saccadic
# rate, the type of stimulus has a significant impact
# the effect of stimulus type is particularly strong when participants are 
# tracking the stimulus with their eyes only, indicating a significant 
# interaction between condition and stimulus type











