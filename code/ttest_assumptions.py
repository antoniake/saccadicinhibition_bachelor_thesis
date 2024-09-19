import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# paired t-test assumptions: normality of differences, independence of pairs

## normality hyp 1

file_path_1 = '../results/df_hypothesis1.csv'
df_1 = pd.read_csv(file_path_1)

# normality with qq plot
def check_normality(df, group_cols, value_col):
    grouped = df.groupby(group_cols)
    for name, group in grouped:
        print(f'Checking normality for group: {name}')
        shapiro_test = stats.shapiro(group[value_col])
        print(f'Shapiro-Wilk test p-value: {shapiro_test.pvalue}')
        
        plt.figure(figsize=(8, 6))
        stats.probplot(group[value_col], dist="norm", plot=plt)
        plt.title(f'Q-Q plot for group: {name}')
        plt.show()

check_normality(df_1, ['condition', 'stimulus type'], 'mean')

## normality hyp 2

file_path_2 = './df_hypothesis2.csv'
df_2 = pd.read_csv(file_path_2)

check_normality(df_2, ['condition', 'stimulus type'], 'mean')


