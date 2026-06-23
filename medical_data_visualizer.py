import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import the data from medical_examination.csv
df = pd.read_csv('medical_examination.csv')

# 2. Add an overweight column
# Formula: weight (kg) / (height (m) ** 2). Note: height is given in cm, so we divide by 100.
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

# 3. Normalize data by making 0 always good and 1 always bad
# If cholesterol or gluc is 1, make it 0. If it's greater than 1, make it 1.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4. Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    # 5. Create a DataFrame for the cat plot using pd.melt
    df_cat = pd.melt(
        df, 
        id_vars=['cardio'], 
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    # 6. Group and reformat the data to split it by cardio and show the counts
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    
    # 7. Convert data into long format and create the chart using sns.catplot()
    cat_plot = sns.catplot(
        x='variable', 
        y='total', 
        hue='value', 
        col='cardio', 
        data=df_cat, 
        kind='bar'
    )

    # 8. Get the figure for the output
    fig = cat_plot.fig

    # 9. Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# 10. Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    # 11. Clean the data by filtering out incorrect pressure and percentile outliers
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. Calculate the correlation matrix
    corr = df_heat.corr()

    # 13. Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # 15. Plot the correlation matrix using sns.heatmap()
    sns.heatmap(
        corr, 
        mask=mask, 
        annot=True, 
        fmt='.1f', 
        center=0, 
        vmin=-0.1, 
        vmax=0.25, 
        square=True, 
        linewidths=.5, 
        cbar_kws={'shrink': .45, 'format': '%.2f'}
    )

    # 16. Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig


