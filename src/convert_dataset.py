import pandas as pd
import glob

def convert_to_poll_format():
    files = glob.glob("data/*.csv")

    all_data = []

    for file in files:
        df = pd.read_csv(file)

        # 🔍 Detect country column
        if "Country" in df.columns:
            country_col = "Country"
        elif "Country or region" in df.columns:
            country_col = "Country or region"
        else:
            print(f"⚠️ Skipping file (no country column): {file}")
            continue

        # 🔍 Detect region column
        if "Region" in df.columns:
            region_col = "Region"
        else:
            region_col = None

        # 🔍 Detect score column
        if "Happiness Score" in df.columns:
            score_col = "Happiness Score"
        elif "Score" in df.columns:
            score_col = "Score"
        else:
            print(f"⚠️ Skipping file (no score column): {file}")
            continue

        for i, row in df.iterrows():
            score = row[score_col]

            # Convert score → poll option
            if score > 7:
                option = "Very Happy"
            elif score > 6:
                option = "Happy"
            elif score > 5:
                option = "Neutral"
            else:
                option = "Unhappy"

            all_data.append({
                "respondent_id": f"{row[country_col]}_{i}",
                "region": row[region_col] if region_col else "Unknown",
                "question": "How happy are people in your country?",
                "option": option
            })

    final_df = pd.DataFrame(all_data)
    final_df.to_csv("data/poll_converted.csv", index=False)

    print("✅ Converted dataset saved as data/poll_converted.csv")

if __name__ == "__main__":
    convert_to_poll_format()