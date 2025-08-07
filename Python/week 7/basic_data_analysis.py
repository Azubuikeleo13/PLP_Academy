# Analyzing Data with Pandas and Visualizing Results with Matplotlib
# Dataset: Iris dataset from sklearn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# Optional: Display plots inline if using a notebook
# %matplotlib inline

# -------------------------------
# Task 1: Load and Explore the Dataset
# -------------------------------

try:
    # Load the iris dataset
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    
    print("✅ Dataset loaded successfully.\n")
    
except Exception as e:
    print(f"❌ Failed to load the dataset: {e}")

# Display first 5 rows
print("🔹 First few rows of the dataset:")
print(df.head())

# Check data types and missing values
print("\n🔹 Data types:")
print(df.dtypes)

print("\n🔹 Missing values in each column:")
print(df.isnull().sum())

# Since Iris has no missing values, we just ensure it's clean

# -------------------------------
# Task 2: Basic Data Analysis
# -------------------------------

# Descriptive statistics
print("\n🔹 Basic statistics of the dataset:")
print(df.describe())

# Group by species and calculate mean
print("\n🔹 Mean values grouped by species:")
grouped = df.groupby('species').mean()
print(grouped)

# Identify interesting patterns
print("\n🔍 Observations:")
print("• Setosa has noticeably smaller petal length and width compared to the other species.")
print("• Virginica tends to have the largest petal dimensions overall.")
print("• Sepal dimensions vary less dramatically between species.")

# -------------------------------
# Task 3: Data Visualization
# -------------------------------

# Set a consistent style
sns.set_theme(style="whitegrid")

# 1. Line chart: Mean petal length per species (not a time series, but shows trend across categories)
plt.figure()
grouped['petal length (cm)'].plot(kind='line', marker='o')
plt.title('Average Petal Length by Species')
plt.xlabel('Species')
plt.ylabel('Petal Length (cm)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Bar chart: Average sepal width per species
plt.figure()
grouped['sepal width (cm)'].plot(kind='bar', color='skyblue')
plt.title('Average Sepal Width by Species')
plt.xlabel('Species')
plt.ylabel('Sepal Width (cm)')
plt.tight_layout()
plt.show()

# 3. Histogram: Distribution of petal length
plt.figure()
plt.hist(df['petal length (cm)'], bins=15, color='coral', edgecolor='black')
plt.title('Distribution of Petal Length')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 4. Scatter plot: Sepal Length vs. Petal Length
plt.figure()
sns.scatterplot(data=df, x='sepal length (cm)', y='petal length (cm)', hue='species', palette='deep')
plt.title('Sepal Length vs. Petal Length by Species')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.tight_layout()
plt.show()

# -------------------------------
# Final Notes
# -------------------------------

print("\n📌 Summary:")
print("• Dataset was loaded successfully and had no missing values.")
print("• Descriptive stats and group analysis revealed key differences among species.")
print("• Visualizations clearly show how features vary across the three iris species.")
