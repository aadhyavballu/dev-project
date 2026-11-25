
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
<<<<<<< HEAD
from pathlib import Path

CHART_DIR = Path("outputs") / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)
=======
>>>>>>> 635b4ac (Updated project)

# ==========================================
# 1. INITIALIZATION
# ==========================================

sns.set_theme(style="whitegrid")

OUTPUT = Path("outputs")
CHARTS = OUTPUT / "charts"

OUTPUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

print("\n======================================")
print(" BANGALORE ROUTES DATA ANALYSIS")
print("======================================")

# ==========================================
# 2. LOAD DATASET
# ==========================================

df_raw = pd.read_excel(
<<<<<<< HEAD
    "bangalore_routes1.xlsx",
=======
    "bangalore_routes.xlsx",
>>>>>>> 635b4ac (Updated project)
    sheet_name="bangalore_routes"
)

df_raw.columns = df_raw.columns.astype(str).str.strip()
<<<<<<< HEAD

df = df_raw.copy()

print("\nDATASET LOADED SUCCESSFULLY")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst Five Records:")
print(df.head())

print("\nDataset Information:")
df.info()

# ==========================================
# 3. DATA TYPE HANDLING
# ==========================================

numeric_columns = [
    "lat_src", "lon_src", "lat_dest", "lon_dest",
    "distance", "hour", "is_peak", "road_capacity",
    "vehicles", "speed", "signal_time", "travel_time"
]

categorical_columns = [
    "source_location",
    "destination_location",
    "day_of_week",
    "weather"
]

=======

df = df_raw.copy()

print("\nDATASET LOADED SUCCESSFULLY")
print("Dataset Shape:", df.shape)

print("\nFIRST FIVE RECORDS")
print(df.head())

print("\nDATASET INFORMATION")
df.info()

# Check required columns
numeric_columns = [
    "lat_src", "lon_src", "lat_dest", "lon_dest",
    "distance", "hour", "is_peak", "road_capacity",
    "vehicles", "speed", "signal_time", "travel_time"
]

categorical_columns = [
    "source_location",
    "destination_location",
    "day_of_week",
    "weather"
]

required_columns = numeric_columns + categorical_columns

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns in dataset: {missing_columns}"
    )

# ==========================================
# 3. DATA TYPE CONVERSION
# ==========================================

>>>>>>> 635b4ac (Updated project)
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in categorical_columns:
    df[col] = df[col].astype("string").str.strip()

<<<<<<< HEAD
# Convert blank strings and common placeholders into missing values.
=======
# Replace blank strings and common placeholders
>>>>>>> 635b4ac (Updated project)
df = df.replace(
    ["", "NA", "N/A", "NULL", "null", "None", "-", "--", "?"],
    np.nan
)

# ==========================================
# 4. MISSING VALUE ANALYSIS
# ==========================================

print("\nMISSING VALUES BEFORE CLEANING")

missing_before = df.isnull().sum()

print(missing_before)

# ==========================================
# 5. DUPLICATE REMOVAL
# ==========================================

duplicates = df.duplicated().sum()

print("\nDUPLICATE RECORDS:", duplicates)

df = df.drop_duplicates().copy()

# ==========================================
# 6. INVALID ENTRY DETECTION
# ==========================================

invalid_records = []

# Coordinate validation
coordinate_rules = {
    "lat_src": (-90, 90),
    "lat_dest": (-90, 90),
    "lon_src": (-180, 180),
    "lon_dest": (-180, 180)
}

for col, (lower, upper) in coordinate_rules.items():

    invalid = (
        df[col].notna()
        & ~df[col].between(lower, upper)
    )

    invalid_records.append({
<<<<<<< HEAD
        "column": col,
        "invalid_count": int(invalid.sum())
=======
        "Column": col,
        "Invalid Count": int(invalid.sum())
>>>>>>> 635b4ac (Updated project)
    })

    df.loc[invalid, col] = np.nan


# Other numerical validation
invalid_rules = {
    "distance": (0, None),
    "hour": (0, 23),
    "is_peak": (0, 1),
    "road_capacity": (0, None),
    "vehicles": (0, None),
    "speed": (0, None),
    "signal_time": (0, None),
    "travel_time": (0, None)
}

for col, (lower, upper) in invalid_rules.items():

<<<<<<< HEAD
    invalid = df[col].notna() & (df[col] < lower)
=======
    if col == "distance":
        invalid = df[col].notna() & (df[col] <= lower)
    else:
        invalid = df[col].notna() & (df[col] < lower)
>>>>>>> 635b4ac (Updated project)

    if upper is not None:
        invalid |= (
            df[col].notna()
            & (df[col] > upper)
        )

<<<<<<< HEAD
    invalid_records.append({
        "column": col,
        "invalid_count": int(invalid.sum())
=======
    print(f"Invalid entries in {col}: {invalid.sum()}")

    invalid_records.append({
        "Column": col,
        "Invalid Count": int(invalid.sum())
>>>>>>> 635b4ac (Updated project)
    })

    df.loc[invalid, col] = np.nan


# Save invalid entry report
pd.DataFrame(invalid_records).to_csv(
    OUTPUT / "invalid_entries.csv",
    index=False
)

# ==========================================
# 7. MISSING VALUE TREATMENT
# ==========================================

<<<<<<< HEAD
=======
# Fill numerical missing values using median
>>>>>>> 635b4ac (Updated project)
for col in numeric_columns:

    if df[col].isnull().any():

        median_value = df[col].median()

        if pd.notna(median_value):
            df[col] = df[col].fillna(median_value)


<<<<<<< HEAD
=======
# Fill categorical missing values using mode
>>>>>>> 635b4ac (Updated project)
for col in categorical_columns:

    if df[col].isnull().any():

        mode_value = df[col].mode()

        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value.iloc[0])
        else:
            df[col] = df[col].fillna("Unknown")


missing_after = df.isnull().sum()

print("\nMISSING VALUES AFTER CLEANING")
print(missing_after)

<<<<<<< HEAD
# Save before-and-after missing value comparison
pd.DataFrame({
    "Before Cleaning": missing_before,
    "After Cleaning": missing_after
}).to_csv(OUTPUT / "missing_values_comparison.csv")
=======
# Save missing value comparison
pd.DataFrame({
    "Before Cleaning": missing_before,
    "After Cleaning": missing_after
}).to_csv(
    OUTPUT / "missing_values_comparison.csv"
)
>>>>>>> 635b4ac (Updated project)

# ==========================================
# 8. OUTLIER DETECTION USING IQR
# ==========================================

print("\nOUTLIER DETECTION")

outlier_results = []

for col in numeric_columns:

    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

<<<<<<< HEAD
    outliers = df[
        (df[col] < lower) |
        (df[col] > upper)
    ]
=======
    outliers = (
        (df[col] < lower) |
        (df[col] > upper)
    )

    outlier_count = int(outliers.sum())

    print(f"{col}: {outlier_count} outliers")
>>>>>>> 635b4ac (Updated project)

    outlier_results.append({
        "Column": col,
        "Q1": q1,
        "Q3": q3,
        "Lower Bound": lower,
        "Upper Bound": upper,
<<<<<<< HEAD
        "Outlier Count": len(outliers)
    })

    print(f"{col}: {len(outliers)} outliers")


=======
        "Outlier Count": outlier_count
    })

# Outliers are identified, not automatically removed
>>>>>>> 635b4ac (Updated project)
pd.DataFrame(outlier_results).to_csv(
    OUTPUT / "outlier_summary.csv",
    index=False
)

<<<<<<< HEAD
# Outliers are identified, not automatically deleted.

# ==========================================
# 9. SAVE CLEANED DATA
# ==========================================

df.to_csv(
    OUTPUT / "cleaned_bangalore_routes.csv",
=======
# ==========================================
# 9. SAVE CLEANED DATASET
# ==========================================

df.to_csv(
    OUTPUT / "cleaned_data.csv",
>>>>>>> 635b4ac (Updated project)
    index=False
)

df_raw.head(10).to_csv(
    OUTPUT / "before_cleaning.csv",
    index=False
)

df.head(10).to_csv(
    OUTPUT / "after_cleaning.csv",
    index=False
)

<<<<<<< HEAD
print("\nCLEANED DATASET SHAPE:")
print(df.shape)
=======
print("\nCLEANED DATASET SHAPE:", df.shape)
>>>>>>> 635b4ac (Updated project)

# ==========================================
# 10. STATISTICAL SUMMARY
# ==========================================

print("\nSTATISTICAL SUMMARY")

summary = df.describe(include="all")

print(summary)

summary.to_csv(
    OUTPUT / "statistical_summary.csv"
)

# ==========================================
<<<<<<< HEAD
=======
# GRAPH SAVING AND DISPLAY FUNCTION
# ==========================================

def save_chart(filename):

    plt.tight_layout()

    # Save graph
    plt.savefig(
        CHARTS / filename,
        dpi=300,
        bbox_inches="tight"
    )

    # Display graph
    plt.show()

    # Close current figure
    plt.close()

    print(f"Graph saved: {filename}")


# ==========================================
>>>>>>> 635b4ac (Updated project)
# 11. UNIVARIATE ANALYSIS
# ==========================================

# A. Distance Distribution

plt.figure(figsize=(8, 5))

sns.histplot(
<<<<<<< HEAD
    df["distance"],
=======
    df["distance"].dropna(),
>>>>>>> 635b4ac (Updated project)
    kde=True,
    bins=30
)

plt.title("Distribution of Route Distance")
plt.xlabel("Distance")
plt.ylabel("Frequency")

<<<<<<< HEAD
plt.tight_layout()
plt.savefig(CHARTS / "distance_distribution.png")
plt.close()
=======
save_chart("distance_distribution.png")
>>>>>>> 635b4ac (Updated project)


# B. Source Locations

plt.figure(figsize=(10, 6))

df["source_location"].value_counts().head(15).plot(
    kind="bar"
)

plt.title("Top 15 Source Locations")
plt.xlabel("Source Location")
plt.ylabel("Number of Routes")

plt.xticks(rotation=45)
<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "source_locations.png")
plt.close()
=======

save_chart("source_locations.png")
>>>>>>> 635b4ac (Updated project)


# C. Destination Locations

plt.figure(figsize=(10, 6))

df["destination_location"].value_counts().head(15).plot(
    kind="bar"
)

plt.title("Top 15 Destination Locations")
plt.xlabel("Destination Location")
plt.ylabel("Number of Routes")

plt.xticks(rotation=45)
<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "destination_locations.png")
plt.close()
=======

save_chart("destination_locations.png")
>>>>>>> 635b4ac (Updated project)


# D. Travel Time Distribution

plt.figure(figsize=(8, 5))

sns.histplot(
<<<<<<< HEAD
    df["travel_time"],
=======
    df["travel_time"].dropna(),
>>>>>>> 635b4ac (Updated project)
    kde=True,
    bins=30
)

plt.title("Distribution of Travel Time")
plt.xlabel("Travel Time")
plt.ylabel("Frequency")

<<<<<<< HEAD
plt.tight_layout()
plt.savefig(CHARTS / "travel_time_distribution.png")
plt.close()
=======
save_chart("travel_time_distribution.png")
>>>>>>> 635b4ac (Updated project)


# ==========================================
# 12. BIVARIATE ANALYSIS
# ==========================================

# A. Distance vs Travel Time

<<<<<<< HEAD
plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="distance",
    y="travel_time",
    alpha=0.5
=======
# Sample records to keep the scatter plot readable
plot_data = df.sample(
    n=min(20000, len(df)),
    random_state=42
)

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=plot_data,
    x="distance",
    y="travel_time",
    alpha=0.4
>>>>>>> 635b4ac (Updated project)
)

plt.title("Distance vs Travel Time")
plt.xlabel("Distance")
plt.ylabel("Travel Time")

<<<<<<< HEAD
plt.tight_layout()
plt.savefig(CHARTS / "distance_vs_travel_time.png")
plt.close()
=======
save_chart("distance_vs_travel_time.png")
>>>>>>> 635b4ac (Updated project)


# B. Peak vs Non-Peak Travel Time

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=df,
    x="is_peak",
    y="travel_time"
)

plt.title("Peak vs Non-Peak Travel Time")
plt.xlabel("Peak Hour (0 = No, 1 = Yes)")
plt.ylabel("Travel Time")

<<<<<<< HEAD
plt.tight_layout()
plt.savefig(CHARTS / "peak_travel_time.png")
plt.close()
=======
save_chart("peak_travel_time.png")
>>>>>>> 635b4ac (Updated project)


# C. Speed vs Travel Time

plt.figure(figsize=(8, 5))

sns.scatterplot(
<<<<<<< HEAD
    data=df,
    x="speed",
    y="travel_time",
    alpha=0.5
=======
    data=plot_data,
    x="speed",
    y="travel_time",
    alpha=0.4
>>>>>>> 635b4ac (Updated project)
)

plt.title("Speed vs Travel Time")
plt.xlabel("Speed")
plt.ylabel("Travel Time")

<<<<<<< HEAD
plt.tight_layout()
plt.savefig(CHARTS / "speed_vs_travel_time.png")
plt.close()
#distance vs time
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="distance", y="travel_time")
plt.title("Distance vs Travel Time")
plt.xlabel("Distance")
plt.ylabel("Travel Time")
plt.savefig(CHART_DIR / "15_distance_vs_travel_time.png")
plt.close()
#average speed by day
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="day_of_week", y="speed")
plt.title("Average Speed by Day")
plt.xticks(rotation=30)
plt.savefig(CHART_DIR / "16_speed_by_day.png")
plt.close()
vehicle cont by hour 
plt.figure(figsize=(8, 5))
sns.lineplot(data=df, x="hour", y="vehicles", estimator="mean")
plt.title("Average Vehicle Count by Hour")
plt.savefig(CHART_DIR / "17_vehicles_by_hour.png")
plt.close()
#travel time
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="weather", y="travel_time")
plt.title("Average Travel Time by Weather")
plt.xticks(rotation=30)
plt.savefig(CHART_DIR / "18_travel_time_by_weather.png")
plt.close()
#distance distibution
plt.figure(figsize=(8, 5))
sns.histplot(df["distance"], bins=30, kde=True)
plt.title("Distribution of Route Distance")
plt.xlabel("Distance")
plt.savefig(CHART_DIR / "19_distance_distribution.png")
plt.close()
=======
save_chart("speed_vs_travel_time.png")
>>>>>>> 635b4ac (Updated project)


# ==========================================
# 13. MULTIVARIATE ANALYSIS
# ==========================================

<<<<<<< HEAD
=======
# A. Correlation Heatmap

>>>>>>> 635b4ac (Updated project)
plt.figure(figsize=(12, 8))

correlation = df[numeric_columns].corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "correlation_heatmap.png")
plt.close()


# A. Travel Time by Hour
=======
save_chart("correlation_heatmap.png")

correlation.to_csv(
    OUTPUT / "correlation_matrix.csv"
)


# B. Average Travel Time by Hour
>>>>>>> 635b4ac (Updated project)

hourly = df.groupby("hour")["travel_time"].mean()

plt.figure(figsize=(9, 5))

hourly.plot(marker="o")

plt.title("Average Travel Time by Hour")
plt.xlabel("Hour")
plt.ylabel("Average Travel Time")

<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "travel_time_by_hour.png")
plt.close()


# B. Travel Time by Weather
=======
save_chart("travel_time_by_hour.png")


# C. Average Travel Time by Weather
>>>>>>> 635b4ac (Updated project)

weather = df.groupby("weather")["travel_time"].mean()

plt.figure(figsize=(8, 5))

weather.plot(kind="bar")

plt.title("Average Travel Time by Weather")
plt.xlabel("Weather")
plt.ylabel("Average Travel Time")

<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "travel_time_by_weather.png")
plt.close()


# C. Travel Time by Day
=======
plt.xticks(rotation=30)

save_chart("travel_time_by_weather.png")


# D. Average Travel Time by Day
>>>>>>> 635b4ac (Updated project)

day = df.groupby("day_of_week")["travel_time"].mean()

plt.figure(figsize=(9, 5))

day.plot(kind="bar")

plt.title("Average Travel Time by Day of Week")
plt.xlabel("Day")
plt.ylabel("Average Travel Time")

<<<<<<< HEAD
plt.tight_layout()

plt.savefig(CHARTS / "travel_time_by_day.png")
plt.close()
=======
plt.xticks(rotation=30)

save_chart("travel_time_by_day.png")


# E. Average Speed by Day

speed_day = df.groupby("day_of_week")["speed"].mean()

plt.figure(figsize=(9, 5))

speed_day.plot(kind="bar")

plt.title("Average Speed by Day")
plt.xlabel("Day of Week")
plt.ylabel("Average Speed")

plt.xticks(rotation=30)

save_chart("average_speed_by_day.png")


# F. Average Vehicle Count by Hour

vehicles_hour = df.groupby("hour")["vehicles"].mean()

plt.figure(figsize=(9, 5))

vehicles_hour.plot(marker="o")

plt.title("Average Vehicle Count by Hour")
plt.xlabel("Hour")
plt.ylabel("Average Number of Vehicles")

save_chart("vehicles_by_hour.png")
>>>>>>> 635b4ac (Updated project)


# ==========================================
# 14. ROUTE ANALYSIS
# ==========================================

routes = (
    df.groupby([
        "source_location",
        "destination_location"
    ])
    .size()
    .sort_values(ascending=False)
)

print("\nTOP 10 ROUTES")

print(routes.head(10))

routes.head(10).to_csv(
    OUTPUT / "top_10_routes.csv"
)


# ==========================================
# 15. ADDITIONAL ANALYSIS
# ==========================================

# Weather vs Peak Hour

weather_peak = pd.crosstab(
    df["weather"],
    df["is_peak"]
)

weather_peak.to_csv(
    OUTPUT / "weather_vs_peak.csv"
)

<<<<<<< HEAD
=======

>>>>>>> 635b4ac (Updated project)
# Day vs Weather

day_weather = pd.crosstab(
    df["day_of_week"],
    df["weather"]
)

day_weather.to_csv(
    OUTPUT / "day_vs_weather.csv"
)

<<<<<<< HEAD
# Correlation matrix

correlation.to_csv(
    OUTPUT / "correlation_matrix.csv"
)


# ==========================================
# 16. TEN PROJECT OBJECTIVES
# ==========================================

objectives = [
    "Understand the structure and characteristics of the Bangalore routes dataset.",
    "Identify the most frequently occurring source locations.",
    "Identify the most frequently occurring destination locations.",
    "Analyse the distribution of route distances.",
    "Identify the most frequently recorded source-destination routes.",
    "Compare travel time during peak and non-peak hours.",
    "Study the relationship between distance, speed and travel time.",
    "Analyse travel time variations by hour, day and weather.",
    "Examine relationships among traffic, road capacity, signal time and travel time.",
    "Identify missing values, duplicates, invalid entries and statistical outliers."
]

pd.DataFrame({
    "Objective Number": range(1, 11),
    "Objective": objectives
}).to_csv(
    OUTPUT / "project_objectives.csv",
    index=False
)


# ==========================================
# 17. FINAL RESULTS
=======

# ==========================================
# 16. FINAL RESULTS
>>>>>>> 635b4ac (Updated project)
# ==========================================

print("\n======================================")
print("       ANALYSIS COMPLETED")
print("======================================")

print("\nOriginal Dataset Shape:", df_raw.shape)
<<<<<<< HEAD
print("Final Dataset Shape:", df.shape)

print(
    "\nTotal Missing Values:",
=======

print("Final Dataset Shape:", df.shape)

print(
    "\nTotal Remaining Missing Values:",
>>>>>>> 635b4ac (Updated project)
    df.isnull().sum().sum()
)

print(
    "Remaining Duplicate Records:",
    df.duplicated().sum()
)

<<<<<<< HEAD
print("\nAll charts saved inside outputs/charts/")
print("All analysis tables saved inside outputs/")
=======
print("\nAll graphs saved inside:", CHARTS)

print("All reports saved inside:", OUTPUT)
>>>>>>> 635b4ac (Updated project)

print("\nTHANK YOU!")

