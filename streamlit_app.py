import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Product Preference Survey Analysis Dashboard", layout="wide")

st.title("📊 Product Preference Survey Analysis Dashboard")

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("data/poll_data.csv")

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region", df["Region"].unique(), default=df["Region"].unique()
)

age = st.sidebar.multiselect(
    "Select Age Group", df["Age_Group"].unique(), default=df["Age_Group"].unique()
)

filtered_df = df[(df["Region"].isin(region)) & (df["Age_Group"].isin(age))]

# -----------------------
# SUMMARY
# -----------------------
st.subheader("📌 Summary")

vote_counts = filtered_df["Response"].value_counts()
vote_percent = filtered_df["Response"].value_counts(normalize=True) * 100

summary = pd.DataFrame({
    "Votes": vote_counts,
    "Percentage": vote_percent
})

st.dataframe(summary)

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(filtered_df))
col2.metric("Top Product", vote_counts.idxmax())
col3.metric("Least Product", vote_counts.idxmin())

# Download Button
st.download_button(
    label="Download Summary",
    data=summary.to_csv().encode('utf-8'),
    file_name='poll_summary.csv',
    mime='text/csv'
)

# -----------------------
# BAR CHART
# -----------------------
st.subheader("📊 Vote Count")

fig1, ax1 = plt.subplots()
sns.barplot(x=vote_counts.index, y=vote_counts.values, ax=ax1)
st.pyplot(fig1)

# -----------------------
# PIE CHART
# -----------------------
st.subheader("🥧 Vote Share")

fig2, ax2 = plt.subplots()
ax2.pie(vote_counts, labels=vote_counts.index, autopct='%1.1f%%')
st.pyplot(fig2)

# -----------------------
# REGION ANALYSIS
# -----------------------
st.subheader("🌍 Region-wise Analysis")

region_analysis = pd.crosstab(filtered_df["Region"], filtered_df["Response"])
st.bar_chart(region_analysis)

# -----------------------
# AGE ANALYSIS
# -----------------------
st.subheader("👥 Age Group Analysis")

age_analysis = pd.crosstab(filtered_df["Age_Group"], filtered_df["Response"])
st.bar_chart(age_analysis)

# -----------------------
# SMART INSIGHTS
# -----------------------
st.subheader("📊 Advanced Insights")

if not vote_counts.empty:
    top_choice = vote_counts.idxmax()
    least_choice = vote_counts.idxmin()

    st.write(f"✅ Most Preferred Product: {top_choice}")
    st.write(f"❌ Least Preferred Product: {least_choice}")

    # Region-wise winner
    region_winner = region_analysis.idxmax(axis=1)
    st.write("🌍 Top Product by Region:")
    st.dataframe(region_winner)

    # Age-wise winner
    age_winner = age_analysis.idxmax(axis=1)
    st.write("👥 Top Product by Age Group:")
    st.dataframe(age_winner)

st.markdown("""
### 📌 Business Insights

- Product C leads overall but competition is very close.
- Different regions show varied preferences → targeted marketing needed.
- Age groups show different trends → segmentation strategy possible.
""")