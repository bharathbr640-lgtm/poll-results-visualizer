# src/analysis.py
import pandas as pd
import numpy as np

def compute_overall_share(df, question=None):
    """
    For a question, compute counts and percentage share per option.
    Returns DataFrame with columns: option, count, pct
    """
    if question:
        dfq = df[df['question'] == question]
    else:
        dfq = df.copy()

    total = len(dfq)
    summary = dfq.groupby('option').size().reset_index(name='count').sort_values('count', ascending=False)
    summary['pct'] = (summary['count'] / total * 100).round(2)
    summary = summary.reset_index(drop=True)
    return summary, total

def compute_demographic_breakdown(df, question, demographic_col):
    """
    Return pivot table: index = demographic values (region/age_group/gender), columns=option, values=percentage
    """
    dfq = df[df['question'] == question]
    pivot = (dfq.groupby([demographic_col, 'option']).size()
             .groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
             .unstack(fill_value=0).round(2))
    return pivot

def compute_trends(df, question, freq='D'):
    """
    Time series trend: counts per option at given frequency (D=day, W=week).
    Only runs if timestamp exists.
    """
    if 'timestamp' not in df.columns:
        print("⚠️ No timestamp column found. Skipping trend analysis.")
        return None, None

    dfq = df[df['question'] == question].copy()
    dfq = dfq.dropna(subset=['timestamp'])

    if dfq.empty:
        print("⚠️ No valid timestamp data available.")
        return None, None

    dfq.set_index('timestamp', inplace=True)

    trend = dfq.groupby([pd.Grouper(freq=freq), 'option']).size().unstack(fill_value=0)
    trend_pct = trend.div(trend.sum(axis=1), axis=0).fillna(0) * 100

    return trend, trend_pct