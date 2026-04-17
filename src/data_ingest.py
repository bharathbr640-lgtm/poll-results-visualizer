# src/data_ingest.py
import pandas as pd

def load_data(csv_path="data/poll_responses.csv"):
    """
    Loads CSV into DataFrame. If the CSV doesn't exist, raise informative error.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Run data generator or provide dataset.") from e
    return df