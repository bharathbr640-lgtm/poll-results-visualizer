"""
Run the entire Poll Results Visualizer pipeline:
1) Load converted poll data
2) Clean
3) Analysis (overall share, demographics, trend if available)
4) Visualizations saved to outputs/
5) Summary insights saved to outputs/insights.txt
"""

import os
from src.data_ingest import load_data
from src.preprocess import clean_data
from src.analysis import compute_overall_share, compute_demographic_breakdown, compute_trends
from src.visualize import plot_bar, plot_pie, plot_stacked_by_region, plot_trend


def save_insights(text, path="outputs/insights.txt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    os.makedirs("outputs", exist_ok=True)

    print("1) Loading data...")
    df = load_data("data/poll_converted.csv")

    print("2) Cleaning data...")
    df_clean = clean_data(df)
    df_clean.to_csv("outputs/cleaned_data.csv", index=False)
    print(" -> saved outputs/cleaned_data.csv")

    question = df_clean["question"].unique()[0]
    print("Question:", question)

    print("3) Overall analysis...")
    summary, total = compute_overall_share(df_clean, question=question)
    summary.to_csv("outputs/summary_table.csv", index=False)
    print(f" -> saved outputs/summary_table.csv (total responses: {total})")

    print("4) Demographic breakdown (region)...")
    pivot_region = compute_demographic_breakdown(df_clean, question=question, demographic_col="region")
    pivot_region.to_csv("outputs/region_pivot.csv")
    print(" -> saved outputs/region_pivot.csv")

    print("5) Trend analysis...")
    trend_counts, trend_pct = compute_trends(df_clean, question=question, freq="D")

    if trend_counts is not None and trend_pct is not None:
        trend_counts.to_csv("outputs/trend_counts.csv")
        trend_pct.to_csv("outputs/trend_pct.csv")
        print(" -> saved trend outputs")
    else:
        print(" -> trend analysis skipped")

    print("6) Visualizations...")
    plot_bar(summary, title="Overall Option Counts", outpath="outputs/bar_chart.png")
    plot_pie(summary, title="Overall Option Share", outpath="outputs/pie_chart.png")
    plot_stacked_by_region(pivot_region, title="Option Distribution by Region", outpath="outputs/stacked_region.png")

    if trend_pct is not None:
        plot_trend(trend_pct, title="Daily Option Share Trend", outpath="outputs/trend_chart.png")

    print(" -> saved charts in outputs/")

    print("7) Summary insights...")
    leader = summary.iloc[0]
    second = summary.iloc[1] if len(summary) > 1 else None

    insight_text = (
        f"Summary Insights\n"
        f"Total responses: {total}\n\n"
        f"Top option: {leader['option']} with {leader['count']} votes ({leader['pct']}%).\n"
    )

    if second is not None:
        diff = leader["pct"] - second["pct"]
        insight_text += f"Lead over second ({second['option']}): {diff:.2f} percentage points.\n\n"

    for region in pivot_region.index:
        opt = pivot_region.loc[region].idxmax()
        pct = pivot_region.loc[region].max()
        insight_text += f"Region {region}: leader = {opt} ({pct}%).\n"

    save_insights(insight_text)
    print(" -> saved outputs/insights.txt")

    print("Done. Check the outputs/ folder for charts, CSVs and insights.")


if __name__ == "__main__":
    main()