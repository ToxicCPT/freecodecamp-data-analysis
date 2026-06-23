import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def draw_plot():
    # 1. Import data from epa-sea-level.csv
    df = pd.read_csv('epa-sea-level.csv')

    # 2. Create scatter plot using Year and CSIRO Adjusted Sea Level
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], color='blue', alpha=0.6, label='Historical Data')

    # 3. First Line of Best Fit (All historical data from 1880 to present)
    # Calculate slope and intercept
    res_all = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Create an extended timeline arrays running all the way out to 2050
    years_extended_all = np.arange(df['Year'].min(), 2051)
    
    # Linear equation formula: y = mx + c (slope * x + intercept)
    line_all = res_all.slope * years_extended_all + res_all.intercept
    plt.plot(years_extended_all, line_all, color='red', label='Trendline (1880-2050)')

    # 4. Second Line of Best Fit (Modern trend data from Year 2000 to present)
    # Filter dataset for modern records
    df_modern = df[df['Year'] >= 2000]
    res_modern = linregress(df_modern['Year'], df_modern['CSIRO Adjusted Sea Level'])
    
    # Create extended timeline starting from 2000 running out to 2050
    years_extended_modern = np.arange(2000, 2051)
    
    # Calculate values for modern prediction line
    line_modern = res_modern.slope * years_extended_modern + res_modern.intercept
    plt.plot(years_extended_modern, line_modern, color='green', label='Modern Trendline (2000-2050)')

    # 5. Add labels, title, and legend structure
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()

    # Save plot and return the active figure object
    plt.savefig('sea_level_plot.png')
    return plt.gca()

