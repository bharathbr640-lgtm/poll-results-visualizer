# src/preprocess.py
import pandas as pd
from dateutil import parser

def clean_data(df):
    """
    Basic cleaning steps:
    - parse timestamps
    - drop duplicates
    - trim whitespace
    - standardize category names (lowercase or title case)
    """
    df = df.copy()
    # strip whitespace from string columns
    str_cols = df.select_dtypes(include=['object']).columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()

    # parse timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        # drop rows with invalid timestamps
        df = df[~df['timestamp'].isna()]

    # drop duplicate respondent for same question
    df = df.drop_duplicates(subset=['respondent_id', 'question'], keep='last')

    # ensure categorical types for memory and consistent ordering
    # Convert columns only if they exist
    if 'region' in df.columns:
        df['region'] = df['region'].astype('category')

    if 'age_group' in df.columns:
        df['age_group'] = df['age_group'].astype('category')

    if 'gender' in df.columns:
        df['gender'] = df['gender'].astype('category')

    if 'option' in df.columns:
        df['option'] = df['option'].astype('category')

    return df