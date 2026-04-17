# src/data_generator.py
"""
Generate synthetic poll dataset (CSV) for Poll Results Visualizer.
Columns:
- respondent_id, timestamp, region, age_group, gender, question, option
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_poll(n_respondents=2000, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    regions = ['North', 'South', 'East', 'West', 'Central']
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    genders = ['Male', 'Female', 'Other']

    # Example poll: single-question multi-option (can expand to multiple questions)
    question = "Which product would you prefer for your next purchase?"
    options = ['Product A', 'Product B', 'Product C', 'Product D']

    # introduce region-wise preference bias
    region_bias = {
        'North': [0.35, 0.25, 0.2, 0.2],
        'South': [0.2, 0.4, 0.25, 0.15],
        'East':  [0.25, 0.25, 0.35, 0.15],
        'West':  [0.15, 0.3, 0.2, 0.35],
        'Central':[0.3, 0.2, 0.2, 0.3]
    }

    start_date = datetime.now() - timedelta(days=30)
    rows = []
    for i in range(n_respondents):
        respondent_id = f"R{i+1:05d}"
        ts = start_date + timedelta(minutes=random.randint(0, 30*24*60))
        region = random.choices(regions, weights=[20,20,20,20,20], k=1)[0]
        age = random.choices(age_groups, weights=[20,30,25,15,10], k=1)[0]
        gender = random.choices(genders, weights=[45,45,10], k=1)[0]

        # pick option with region bias + slight age bias
        base_probs = np.array(region_bias[region])
        if age == '18-24':
            base_probs = base_probs * np.array([1.1, 1.0, 0.9, 1.0])
        base_probs = base_probs / base_probs.sum()
        option = random.choices(options, weights=base_probs, k=1)[0]

        rows.append({
            'respondent_id': respondent_id,
            'timestamp': ts.isoformat(),
            'region': region,
            'age_group': age,
            'gender': gender,
            'question': question,
            'option': option
        })

    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df = generate_synthetic_poll(2000)
    df.to_csv("data/poll_responses.csv", index=False)
    print("Synthetic dataset saved to data/poll_responses.csv")