import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import math

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',index_col='date')
df.index = pd.to_datetime(df.index)
# Clean data

twoPointFivePercent = math.ceil((len(df.index) * 2.5) / 100) # 2.5%

df = df.sort_values(by='value') # Sort by value
df = df.iloc[twoPointFivePercent:-twoPointFivePercent] # Remove top 2.5% and low 2.5%
df = df.sort_index() # Sort by date


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20,5))

    ax.plot(df.index, df['value'])

    ax.set(xlabel='Date', ylabel='Page Views',
       title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['month'] = df.index.month
    df['year'] = df.index.year
    df_bar = df.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    x = np.arange(len(df_bar.index))  # the label locations
    width = 0.05  # the width of the bars

    fig, ax = plt.subplots()
    ax.set_label('Months')
    ax.bar(x - width*6, df_bar[1], width, label='January')
    ax.bar(x - width*5, df_bar[2], width, label='February')
    ax.bar(x - width*4, df_bar[3], width, label='March')
    ax.bar(x - width*3, df_bar[4], width, label="April")
    ax.bar(x - width*2, df_bar[5], width, label='May')
    ax.bar(x - width, df_bar[6], width, label='June')
    ax.bar(x , df_bar[7], width, label='July')
    ax.bar(x + width, df_bar[8], width, label="August")
    ax.bar(x + width*2, df_bar[9], width, label='September')
    ax.bar(x + width*3, df_bar[10], width, label='October')
    ax.bar(x + width*4, df_bar[11], width, label='November')
    ax.bar(x + width*5, df_bar[12], width, label="December")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Average Page Views')
    ax.set_xlabel('Years')
    ax.set_xticks(x)
    ax.set_xticklabels(df_bar.index)
    ax.legend(title="Months")
    

    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values(by='month_num')
    fig, axes = plt.subplots(1,2,figsize=(20,5))

    
    sns.boxplot(ax=axes[0], x=df_box['year'], y=df_box['value'])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_ylabel('Page Views')
    axes[0].set_xlabel('Year')

    sns.boxplot(ax=axes[1], x=df_box['month'], y=df_box['value'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_ylabel('Page Views')
    axes[1].set_xlabel('Month')
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig