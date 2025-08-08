""" COVID-19 Global Data Tracker
    Author: Leo Azubuike
    Project Goal: Analyze COVID-19 data globally using Pandas, Matplotlib, and Seaborn
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

# Optional: Set styles
sns.set_theme(style='darkgrid')

# -----------------------------
# 1️⃣ Data Collection & Loading
# -----------------------------

try:
    # Load COVID-19 data from Our World in Data
    url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
    df = pd.read_csv(url)
    # df = pd.read_csv('compact.csv')
    print("✅ Dataset loaded successfully.")
except:
    print("❌ Link not found. Ensure the url is not changed")
    exit()

# -----------------------------
# 2️⃣ Data Exploration
# -----------------------------

print("\n🔍 Preview of dataset:")
print(df.head())

print("\n📊 Column names:")
print(df.columns.tolist())

print("\n🧼 Missing values (top 10 columns with most missing):")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# -----------------------------
# 3️⃣ Data Cleaning
# -----------------------------

# Keep only relevant countries
countries = ['Kenya', 'United States', 'India', 'Nigeria']
df = df[df['country'].isin(countries)]

# Drop rows with missing critical data
df = df.dropna(subset=['date', 'total_cases'])

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Fill missing values in numeric columns
numeric_cols = ['total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
df[numeric_cols] = df[numeric_cols].fillna(0)

# -----------------------------
# 4️⃣ Exploratory Data Analysis (EDA)
# -----------------------------

# Total Cases Over Time
plt.figure(figsize=(10,6))
for country in countries:
    country_data = df[df['country'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()

# Total Deaths Over Time
plt.figure(figsize=(10,6))
for country in countries:
    country_data = df[df['country'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)

plt.title('Total COVID-19 Deaths Over Time')
plt.xlabel('Date')
plt.ylabel('Total Deaths')
plt.legend()
plt.tight_layout()
plt.show()

# Daily New Cases Comparison
plt.figure(figsize=(10,6))
for country in countries:
    country_data = df[df['country'] == country]
    plt.plot(country_data['date'], country_data['new_cases'], label=country)

plt.title('Daily New COVID-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend()
plt.tight_layout()
plt.show()

# Calculate death rate
df['death_rate'] = df['total_deaths'] / df['total_cases']
death_rate_df = df.groupby('country')['death_rate'].mean().reset_index()

# -----------------------------
# 5️⃣ Vaccination Progress
# -----------------------------

plt.figure(figsize=(10,6))
for country in countries:
    country_data = df[df['country'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title('Total Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------
# 6️⃣ Key Insights
# -----------------------------

print("\n📌 Key Insights:")
print("• The United States had a significant early lead in both cases and vaccinations.")
print("• India shows a massive spike in cases during the 2021 wave, with a slower vaccine rollout.")
print("• Nigeria’s and Kenya’s reported numbers are lower, potentially due to testing or reporting limitations.")
print("• Vaccination curves show steady growth, but with large gaps between countries.")
print("• Death rate varies slightly, likely due to healthcare systems and data accuracy.")

# -----------------------------
# 7️⃣ Export (Optional)
# -----------------------------

# OPtional: Save cleaned data for reuse
# df.to_csv('cleaned_covid_data.csv', index=False)
# print("\n📁 Cleaned dataset saved as 'cleaned_covid_data.csv'.")


# -----------------------------
# 6️⃣ Choropleth Map: COVID-19 Total Cases by Country
# -----------------------------

# If you're using Jupyter Notebook and the maps don’t show, uncomment this line below:
# pio.renderers.default = 'notebook'  # or 'iframe' or 'browser' if needed

# Filter latest data per country (latest date for each country)
latest_df = df.sort_values('date').groupby('country').tail(1)

# Ensure code is present (needed for plotly)
choropleth_data = latest_df[['country', 'code', 'total_cases', 'total_vaccinations', 'date']].dropna(subset=['code'])

# Plot total cases by country
fig_cases = px.choropleth(
    data_frame=choropleth_data,
    locations='code',
    color='total_cases',
    hover_name='country',
    color_continuous_scale='Reds',
    title='🌍 Total COVID-19 Cases by Country (Latest Available)',
    labels={'total_cases': 'Total Cases'}
)

fig_cases.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
fig_cases.show()

# Optional: Choropleth for total vaccinations
fig_vax = px.choropleth(
    data_frame=choropleth_data,
    locations='code',
    color='total_vaccinations',
    hover_name='country',
    color_continuous_scale='Blues',
    title='🌍 Total COVID-19 Vaccinations by Country (Latest Available)',
    labels={'total_vaccinations': 'Total Vaccinations'}
)

fig_vax.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
fig_vax.show()
