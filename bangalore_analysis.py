import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

# Load dataset
df = pd.read_excel(
    "bengRoutes1.xlsx",
    sheet_name="bangalore_routes"
)

print("DATASET INFORMATION")
print("Shape:", df.shape)
print(df.head())
print(df.info())

# 1. Missing Values
print("\nMISSING VALUES")
print(df.isnull().sum())

# 2. Duplicate Records
print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# 3. Data Type Conversion
numeric_columns = [
    "lat_src", "lon_src", "lat_dest", "lon_dest",
    "distance", "hour", "is_peak", "road_capacity",
    "vehicles", "speed", "signal_time", "travel_time"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove duplicate records
df = df.drop_duplicates()

# 4. Handle Missing Values
for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

categorical_columns = [
    "source_location", "destination_location",
    "day_of_week", "weather"
]

for col in categorical_columns:
    df[col] = df[col].fillna(
        df[col].mode()[0] if not df[col].mode().empty else "Unknown"
    )

# 5. Invalid Entry Detection
invalid_rules = {
    "distance": (0, None),
    "hour": (0, 23),
    "is_peak": (0, 1),
    "speed": (0, None),
    "vehicles": (0, None),
    "road_capacity": (0, None),
    "signal_time": (0, None),
    "travel_time": (0, None)
}

for col, (lower, upper) in invalid_rules.items():
    invalid = df[col] < lower

    if upper is not None:
        invalid |= df[col] > upper

    print(f"Invalid entries in {col}: {invalid.sum()}")

    df.loc[invalid, col] = np.nan

# 6. Outlier Detection using IQR
print("\nOUTLIER DETECTION")

for col in numeric_columns:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[
        (df[col] < lower) | (df[col] > upper)
    ]

    print(f"{col}: {len(outliers)} outliers")

# Save cleaned dataset
Path("outputs").mkdir(exist_ok=True)
df.to_csv("outputs/cleaned_data.csv", index=False)

# 7. Statistical Summary
print("\nSTATISTICAL SUMMARY")
print(df.describe())

df.describe().to_csv("outputs/statistical_summary.csv")

# 8. UNIVARIATE ANALYSIS

# Distance distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["distance"], kde=True)
plt.title("Distribution of Route Distance")
plt.xlabel("Distance")
plt.ylabel("Frequency")
plt.savefig("outputs/distance_distribution.png")
plt.close()

# Source locations
plt.figure(figsize=(10, 6))
df["source_location"].value_counts().head(15).plot(kind="bar")
plt.title("Top 15 Source Locations")
plt.xlabel("Source Location")
plt.ylabel("Number of Routes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/source_locations.png")
plt.close()

# Destination locations
plt.figure(figsize=(10, 6))
df["destination_location"].value_counts().head(15).plot(kind="bar")
plt.title("Top 15 Destination Locations")
plt.xlabel("Destination Location")
plt.ylabel("Number of Routes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/destination_locations.png")
plt.close()

# 9. BIVARIATE ANALYSIS

# Travel time vs distance
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="distance", y="travel_time")
plt.title("Travel Time vs Distance")
plt.savefig("outputs/travel_time_distance.png")
plt.close()

# Peak vs non-peak travel time
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="is_peak", y="travel_time")
plt.title("Peak vs Non-Peak Travel Time")
plt.xlabel("Peak Hour (0 = No, 1 = Yes)")
plt.savefig("outputs/peak_travel_time.png")
plt.close()

# Speed vs travel time
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="speed", y="travel_time")
plt.title("Speed vs Travel Time")
plt.savefig("outputs/speed_travel_time.png")
plt.close()

# 10. MULTIVARIATE ANALYSIS

plt.figure(figsize=(12, 8))

correlation = df[numeric_columns].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png")
plt.close()

# Average travel time by hour
hourly = df.groupby("hour")["travel_time"].mean()

plt.figure(figsize=(9, 5))
hourly.plot(marker="o")
plt.title("Average Travel Time by Hour")
plt.xlabel("Hour")
plt.ylabel("Average Travel Time")
plt.savefig("outputs/travel_time_by_hour.png")
plt.close()

# Average travel time by weather
weather = df.groupby("weather")["travel_time"].mean()

plt.figure(figsize=(8, 5))
weather.plot(kind="bar")
plt.title("Travel Time by Weather")
plt.xlabel("Weather")
plt.ylabel("Average Travel Time")
plt.tight_layout()
plt.savefig("outputs/travel_time_weather.png")
plt.close()

# Average travel time by day
day = df.groupby("day_of_week")["travel_time"].mean()

plt.figure(figsize=(9, 5))
day.plot(kind="bar")
plt.title("Travel Time by Day of Week")
plt.xlabel("Day")
plt.ylabel("Average Travel Time")
plt.tight_layout()
plt.savefig("outputs/travel_time_day.png")
plt.close()

# Route frequency
routes = (
    df.groupby(["source_location", "destination_location"])
    .size()
    .sort_values(ascending=False)
)

print("\nTOP 10 ROUTES")
print(routes.head(10))

routes.head(10).to_csv("outputs/top_routes.csv")

# Final dataset information
print("\nFINAL DATASET SHAPE:", df.shape)
print("Remaining missing values:", df.isnull().sum().sum())

print("\nANALYSIS COMPLETED SUCCESSFULLY!")
