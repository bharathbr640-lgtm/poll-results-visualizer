# src/visualize.py
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")


def plot_bar(summary_df, title="Option counts", outpath="outputs/bar_chart.png"):
    """
    summary_df: DataFrame with columns option,count,pct
    """
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=summary_df, x='option', y='count', order=summary_df['option'])

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{int(height)}',
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom')

    plt.title(title)
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.savefig(outpath)
    plt.close()


def plot_pie(summary_df, title="Option share", outpath="outputs/pie_chart.png"):
    plt.figure(figsize=(6, 6))
    plt.pie(summary_df['count'],
            labels=summary_df['option'],
            autopct='%1.1f%%',
            startangle=140)

    plt.title(title)
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.savefig(outpath)
    plt.close()


def plot_stacked_by_region(pivot_df, title="Region-wise distribution", outpath="outputs/stacked_region.png"):
    plt.figure(figsize=(10, 6))
    pivot_df.plot(kind='bar', stacked=True)

    plt.title(title)
    plt.ylabel("Percentage")
    plt.legend(title="Option", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.savefig(outpath)
    plt.close()


def plot_trend(trend_pct_df, title="Trend (percentage)", outpath="outputs/trend_chart.png"):
    plt.figure(figsize=(10, 6))
    trend_pct_df.plot()

    plt.title(title)
    plt.ylabel("Percentage")
    plt.legend(title="Option", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.savefig(outpath)
    plt.close()