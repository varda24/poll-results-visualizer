import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# STEP 1: Generate Synthetic Data
# -------------------------------
np.random.seed(42)

n = 500

data = pd.DataFrame({
    "Respondent_ID": range(1, n+1),
    "Age_Group": np.random.choice(["18-25", "26-35", "36-50"], n),
    "Region": np.random.choice(["North", "South", "East", "West"], n),
    "Question": "Favorite Product",
    "Response": np.random.choice(["Product A", "Product B", "Product C"], n),
    "Date": pd.date_range(start="2024-01-01", periods=n, freq='D')
})

data.to_csv("data/poll_data.csv", index=False)

# -------------------------------
# STEP 2: Load Data
# -------------------------------
df = pd.read_csv("data/poll_data.csv")

# -------------------------------
# STEP 3: Cleaning
# -------------------------------
df.dropna(inplace=True)

# -------------------------------
# STEP 4: Analysis
# -------------------------------
vote_counts = df["Response"].value_counts()
vote_percent = df["Response"].value_counts(normalize=True) * 100

summary = pd.DataFrame({
    "Votes": vote_counts,
    "Percentage": vote_percent
})

print("\nVote Summary:\n", summary)

# -------------------------------
# STEP 5: Visualization
# -------------------------------

# Bar Chart
plt.figure()
sns.barplot(x=vote_counts.index, y=vote_counts.values)
plt.title("Vote Count by Product")
plt.savefig("outputs/bar_chart.png")
plt.close()

# Pie Chart
plt.figure()
plt.pie(vote_counts, labels=vote_counts.index, autopct='%1.1f%%')
plt.title("Vote Share")
plt.savefig("outputs/pie_chart.png")
plt.close()

# Region-wise Analysis
region_analysis = pd.crosstab(df["Region"], df["Response"])

region_analysis.plot(kind='bar', stacked=True)
plt.title("Region-wise Preferences")
plt.savefig("outputs/region_chart.png")
plt.close()

# Age Group Analysis
age_analysis = pd.crosstab(df["Age_Group"], df["Response"])

age_analysis.plot(kind='bar', stacked=True)
plt.title("Age Group Preferences")
plt.savefig("outputs/age_chart.png")
plt.close()

df['Date'] = pd.to_datetime(df['Date'])

trend = df.groupby(['Date', 'Response']).size().unstack()

trend.plot()
plt.title("Trend Over Time")
plt.savefig("outputs/trend_chart.png")
plt.close()
# -------------------------------
# STEP 6: Insights
# -------------------------------
print("\n--- INSIGHTS ---")

top_choice = vote_counts.idxmax()
least_choice = vote_counts.idxmin()

print(f"Most Preferred Option: {top_choice}")
print(f"Least Preferred Option: {least_choice}")

# Region dominance
region_winner = region_analysis.idxmax(axis=1)
print("\nTop Product per Region:\n", region_winner)