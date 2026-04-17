# streamlit_app.py

import streamlit as st
import pandas as pd
from src.preprocess import clean_data
from src.analysis import compute_overall_share, compute_demographic_breakdown
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")

st.title("📊 Poll Results Visualizer")

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload your poll CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using default dataset (poll_converted.csv)")
    df = pd.read_csv("data/poll_converted.csv")

# ---------------------------
# CLEAN DATA
# ---------------------------
df = clean_data(df)

# ---------------------------
# SELECT QUESTION
# ---------------------------
questions = df['question'].unique()
selected_question = st.selectbox("Select Question", questions)

# ---------------------------
# ANALYSIS
# ---------------------------
summary, total = compute_overall_share(df, selected_question)
pivot_region = compute_demographic_breakdown(df, selected_question, 'region')

# ---------------------------
# DISPLAY METRICS
# ---------------------------
st.metric("Total Responses", total)

# ---------------------------
# BAR CHART
# ---------------------------
st.subheader("📊 Overall Results")

fig1, ax1 = plt.subplots()
sns.barplot(data=summary, x='option', y='count', ax=ax1)
st.pyplot(fig1)

# ---------------------------
# PIE CHART
# ---------------------------
st.subheader("🥧 Share Distribution")

fig2, ax2 = plt.subplots()
ax2.pie(summary['count'], labels=summary['option'], autopct='%1.1f%%')
st.pyplot(fig2)

# ---------------------------
# REGION ANALYSIS
# ---------------------------
st.subheader("🌍 Region-wise Analysis")

fig3, ax3 = plt.subplots(figsize=(10,5))
pivot_region.plot(kind='bar', stacked=True, ax=ax3)
st.pyplot(fig3)

# ---------------------------
# INSIGHTS
# ---------------------------
st.subheader("🧠 Insights")

leader = summary.iloc[0]

st.success(f"Top Option: {leader['option']} ({leader['pct']}%)")

for region in pivot_region.index:
    opt = pivot_region.loc[region].idxmax()
    pct = pivot_region.loc[region].max()
    st.write(f"📍 {region}: {opt} ({pct}%)")