
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_theme(style="whitegrid")

# Load Excel dataset
df = pd.read_excel(
    "bangalore_routes.xlsx",
    sheet_name="bangalore_routes"
)

print("\n========== DATASET LOADED ==========")

# Dataset dimensions
print("\nDataset Shape:")
print(df.shape)

# First five records
print("\nFirst Five Records:")
print(df.head())

# Dataset information
print("\nDataset Information:")
df.info()

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

print("\n========== COMPLETED ==========")
