# ======================================
# POLLUTANT CORRELATION HEATMAP
# AUTO-COMPATIBLE WITH CPCB DATA
# ======================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# FILE PATH
# -------------------------------
FILE_PATH = r"E:\Welt Research\2022\Cleaned Data\cleaned_Ashok Vihar.csv"

df = pd.read_csv(FILE_PATH)

print("Data loaded:", df.shape)

# -------------------------------
# SHOW ORIGINAL COLUMNS
# -------------------------------
print("\nOriginal columns:")
print(df.columns.tolist())

# -------------------------------
# RENAME COMMON CPCB NAMES
# -------------------------------
rename_map = {
    'PM2.5 (µg/m³)': 'PM2.5',
    'PM10 (µg/m³)': 'PM10',
    'NO (µg/m³)': 'NO',
    'NO2 (µg/m³)': 'NO2',
    'NOx (ppb)': 'NOx',
    'NH3 (µg/m³)': 'NH3',
    'SO2 (µg/m³)': 'SO2',
    'CO (mg/m³)': 'CO',
    'Ozone (µg/m³)': 'Ozone',
    'AT (°C)': 'Temperature',
    'RH (%)': 'Humidity',
    'WS (m/s)': 'WindSpeed',
    'WD (deg)': 'WindDirection',
    'RF (mm)': 'Rainfall'
}

df.rename(columns=rename_map, inplace=True)

print("\nRenamed columns:")
print(df.columns.tolist())

# -------------------------------
# CREATE AQI IF MISSING
# -------------------------------
if 'AQI' not in df.columns and 'PM2.5' in df.columns and 'PM10' in df.columns:
    df['AQI'] = df[['PM2.5', 'PM10']].max(axis=1)

# -------------------------------
# CREATE MONSOON FLAG
# -------------------------------
date_col = next((c for c in df.columns if 'Date' in c or 'Time' in c), None)

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df['Month'] = df[date_col].dt.month
    df['IsMonsoon'] = df['Month'].isin([6, 7, 8, 9])

# -------------------------------
# SELECT AVAILABLE POLLUTANTS
# -------------------------------
candidate_cols = [
    'PM2.5', 'PM10', 'NO', 'NO2', 'NOx',
    'NH3', 'SO2', 'CO', 'Ozone', 'AQI'
]

pollutant_cols = [c for c in candidate_cols if c in df.columns]

print("\nDetected pollutant columns:", pollutant_cols)

if len(pollutant_cols) < 2:
    raise ValueError("Dataset does not contain enough pollutant columns")

# -------------------------------
# CORRELATION MATRICES
# -------------------------------
corr_matrix = df[pollutant_cols].corr()

if 'IsMonsoon' in df.columns:
    monsoon_corr = df[df['IsMonsoon']][pollutant_cols].corr()
    non_monsoon_corr = df[~df['IsMonsoon']][pollutant_cols].corr()
    diff_corr = monsoon_corr - non_monsoon_corr
else:
    diff_corr = corr_matrix * 0

# -------------------------------
# PLOT HEATMAPS
# -------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle("Pollutant Correlation Analysis", fontsize=16, fontweight='bold')

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# ---- Full Year
sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='RdYlBu_r',
    center=0,
    square=True,
    ax=axes[0],
    linewidths=0.5
)
axes[0].set_title("Full Year Correlation Matrix")

# ---- Monsoon Difference
sns.heatmap(
    diff_corr,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    square=True,
    ax=axes[1],
    linewidths=0.5
)
axes[1].set_title("Correlation Difference (Monsoon - Non-Monsoon)")

plt.tight_layout()

# -------------------------------
# SAVE OUTPUT
# -------------------------------
output_path = r'E:\Welt Research\2021\correlation_analysis.png'
plt.savefig(output_path, dpi=300)
plt.show()

print("Saved to:", output_path)
