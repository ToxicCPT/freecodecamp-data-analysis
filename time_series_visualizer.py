import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Import data and set index to date column
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Clean data by filtering out top 2.5% and bottom 2.5% outliers
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# 3. Draw Line Plot
def draw_line_plot():
    # Copy data to prevent editing the original
    df_line = df.copy()
    
    # Set up matplotlib structure
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    # Style labels and title
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return figure
    fig.savefig('line_plot.png')
    return fig

# 4. Draw Bar Plot
def draw_bar_plot():
    # Copy data and prepare separate year and month columns
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')

    # Group by year and month, calculating average page views
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Order months correctly from Jan to Dec so the legend renders sequentially
    months_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_grouped = df_grouped.reindex(columns=months_order)

    # Plot the grouped bar chart
    fig = df_grouped.plot(kind='bar', figsize=(15, 7), xlabel='Years', ylabel='Average Page Views').figure
    plt.legend(title='Months')

    # Save image and return figure
    fig.savefig('bar_plot.png')
    return fig

# 5. Draw Box Plot
def draw_box_plot():
    # Prepare data for box plots (this code structure is often provided in boilerplate)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Set up side-by-side plot frames
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # First Box Plot: Year-wise Trend
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Second Box Plot: Month-wise Seasonality
    # We sort short month labels cleanly from Jan to Dec
    short_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=short_months, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return figure
    fig.savefig('box_plot.png')
    return fig

