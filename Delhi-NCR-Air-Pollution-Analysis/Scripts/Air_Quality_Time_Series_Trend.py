# ================================
# AIR QUALITY TIME SERIES — ALIPUR 2021
# ================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from matplotlib.lines import Line2D

# 1. LOAD DATA
# -------------------------------
file_path = r'E:\Welt Research\2021\Alipur.csv'   # <-- adjust path if needed
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Rename columns consistently
rename_map = {}
for col in df.columns:
    c = col.lower()
    if 'pm2.5' in c or 'pm25' in c:
        rename_map[col] = 'PM2.5'
    elif 'pm10' in c:
        rename_map[col] = 'PM10'
    elif c == 'date' or 'timestamp' in c:
        rename_map[col] = 'Timestamp'
    elif 'rain' in c:
        rename_map[col] = 'Rainfall'
    elif 'aqi' == c:
        rename_map[col] = 'AQI'
df.rename(columns=rename_map, inplace=True)

# 2. CREATE TIMESTAMP
# -------------------------------
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df = df.dropna(subset=['Timestamp']).sort_values('Timestamp')

# 3. SEASONAL FLAGS
# -------------------------------
df['Month'] = df['Timestamp'].dt.month
df['IsMonsoon'] = df['Month'].isin([6, 7, 8, 9])

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:
        return 'Post-Monsoon'
df['Season'] = df['Month'].apply(get_season)

# 4. HANDLE MISSING VALUES
# -------------------------------
if 'PM2.5' not in df.columns:
    df['PM2.5'] = np.nan
if 'AQI' not in df.columns:
    df['AQI'] = np.nan
if 'Rainfall' not in df.columns:
    df['Rainfall'] = np.nan

df['PM2.5'] = df['PM2.5'].ffill().bfill()
df['AQI'] = df['AQI'].ffill().bfill()
df['Rainfall'] = df['Rainfall'].fillna(0)

# 5. AQI CATEGORY
# -------------------------------
def aqi_category(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Satisfactory'
    elif aqi <= 200: return 'Moderate'
    elif aqi <= 300: return 'Poor'
    elif aqi <= 400: return 'Very Poor'
    else: return 'Severe'
df['AQI_Category'] = df['AQI'].apply(aqi_category)

# 6. VISUALIZATION
# -------------------------------
fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
fig.suptitle('📈 Air Quality Time Series Trends 2021 (Cleaned Data)', 
             fontsize=16, fontweight='bold')

# PM2.5 plot
axes[0].plot(df['Timestamp'], df['PM2.5'], color='#E74C3C', alpha=0.8, linewidth=1.5)
axes[0].fill_between(df['Timestamp'], df['PM2.5'], alpha=0.3, color='#E74C3C')
axes[0].axvspan(pd.Timestamp('2021-06-01'), pd.Timestamp('2021-09-30'),
                alpha=0.2, color='blue', label='Monsoon Season')
axes[0].set_ylabel('PM2.5 (µg/m³)', fontsize=11, fontweight='bold')
axes[0].set_title('PM2.5 Daily Levels', fontsize=12, fontweight='bold', loc='left')
axes[0].legend(loc='upper right')
axes[0].grid(True, alpha=0.3)

# Seasonal averages
for season, color in [('Winter', '#FF6B6B'), ('Spring', '#4ECDC4'),
                      ('Monsoon', '#45B7D1'), ('Post-Monsoon', '#96CEB4')]:
    season_data = df[df['Season'] == season]
    if not season_data.empty:
        axes[0].axhline(y=season_data['PM2.5'].mean(), color=color,
                        linestyle='--', alpha=0.5, linewidth=1.5)

# AQI scatter plot
colors_aqi = df['AQI_Category'].map({
    'Good': '#2ECC71', 'Satisfactory': '#F1C40F', 'Moderate': '#E67E22',
    'Poor': '#E74C3C', 'Very Poor': '#8E44AD', 'Severe': '#C0392B'
})
axes[1].scatter(df['Timestamp'], df['AQI'], c=colors_aqi, s=20, alpha=0.8)
axes[1].axvspan(pd.Timestamp('2021-06-01'), pd.Timestamp('2021-09-30'),
                alpha=0.2, color='blue')
axes[1].set_ylabel('AQI', fontsize=11, fontweight='bold')
axes[1].set_title('AQI Daily Levels (colored by category)', fontsize=12, fontweight='bold', loc='left')
axes[1].grid(True, alpha=0.3)

# AQI guideline lines
for y_val, label, color in [(50, 'Good', 'green'), (100, 'Satisfactory', 'yellow'),
                            (200, 'Moderate', 'orange'), (300, 'Poor', 'red')]:
    axes[1].axhline(y=y_val, color=color, linestyle='--', alpha=0.3, linewidth=1)

# AQI legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Good', markerfacecolor='#2ECC71', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Satisfactory', markerfacecolor='#F1C40F', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Moderate', markerfacecolor='#E67E22', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Poor', markerfacecolor='#E74C3C', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Very Poor', markerfacecolor='#8E44AD', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Severe', markerfacecolor='#C0392B', markersize=8)
]
axes[1].legend(handles=legend_elements, loc='upper right')

# Rainfall bar chart
rainfall_colors = ['lightblue' if r == 0 else 'blue' for r in df['Rainfall']]
axes[2].bar(df['Timestamp'], df['Rainfall'], color=rainfall_colors, alpha=0.7, width=1)
axes[2].axvspan(pd.Timestamp('2021-06-01'), pd.Timestamp('2021-09-30'),
                alpha=0.1, color='blue')
axes[2].set_ylabel('Rainfall (mm)', fontsize=11, fontweight='bold')
axes[2].set_xlabel('Date', fontsize=11, fontweight='bold')
axes[2].set_title('Daily Rainfall', fontsize=12, fontweight='bold', loc='left')
axes[2].grid(True, alpha=0.3, axis='y')

# Format x-axis
axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
axes[2].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.xticks(rotation=45)

plt.tight_layout()
output_path = fr"E:\Welt Research\2021\timeseries_analysis_{datetime.date.today()}.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()
print("✅ Generated:", output_path)
