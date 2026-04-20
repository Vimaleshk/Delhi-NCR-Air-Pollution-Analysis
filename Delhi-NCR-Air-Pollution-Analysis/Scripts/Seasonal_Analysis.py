# ========================================================
# Seasonal and AQI Analysis for Alipur Air Quality Data
# ========================================================

# 1️⃣ Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
sns.set(style="whitegrid")  # nicer plots

# 2️⃣ Load Dataset
file_path = r'E:\Welt Research\2021\Alipur.csv'  # Change path if needed
df = pd.read_csv(file_path)

# Quick check
print("="*60)
print("DATA LOADED SUCCESSFULLY")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())
print("="*60, "\n")

# 3️⃣ Parse datetime and extract features
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Year'] = df['Timestamp'].dt.year
df['Month'] = df['Timestamp'].dt.month
df['Day'] = df['Timestamp'].dt.day
df['DayOfWeek'] = df['Timestamp'].dt.day_name()
df['Season'] = df['Month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring',
    6: 'Monsoon', 7: 'Monsoon', 8: 'Monsoon', 9: 'Monsoon',
    10: 'Post-Monsoon', 11: 'Post-Monsoon'
})

# 4️⃣ Standardize column names
column_mapping = {
    'PM2.5 (µg/m³)': 'PM2.5',
    'PM10 (µg/m³)': 'PM10',
    'NO (µg/m³)': 'NO',
    'NO2 (µg/m³)': 'NO2',
    'NOx (ppb)': 'NOx',
    'NH3 (µg/m³)': 'NH3',
    'SO2 (µg/m³)': 'SO2',
    'CO (mg/m³)': 'CO',
    'Ozone (µg/m³)': 'Ozone',
    'Benzene (µg/m³)': 'Benzene',
    'Toluene (µg/m³)': 'Toluene',
    'Xylene (µg/m³)': 'Xylene',
    'AT (°C)': 'Temperature',
    'RH (%)': 'Humidity',
    'WS (m/s)': 'WindSpeed',
    'WD (deg)': 'WindDirection',
    'RF (mm)': 'Rainfall',
    'TOT-RF (mm)': 'TotalRainfall',
    'SR (W/mt2)': 'SolarRadiation',
    'BP (mmHg)': 'BarometricPressure'
}
df.rename(columns=column_mapping, inplace=True)

# 5️⃣ Calculate AQI (simplified PM2.5 & PM10)
def calculate_aqi_pm25(pm25):
    if pd.isna(pm25):
        return np.nan
    if pm25 <= 30:
        return pm25 * 50 / 30
    elif pm25 <= 60:
        return 50 + (pm25 - 30) * 50 / 30
    elif pm25 <= 90:
        return 100 + (pm25 - 60) * 100 / 30
    elif pm25 <= 120:
        return 200 + (pm25 - 90) * 100 / 30
    elif pm25 <= 250:
        return 300 + (pm25 - 120) * 200 / 130
    else:
        return 400 + (pm25 - 250) * 100 / 130

def calculate_aqi_pm10(pm10):
    if pd.isna(pm10):
        return np.nan
    if pm10 <= 50:
        return pm10 * 50 / 50
    elif pm10 <= 100:
        return 50 + (pm10 - 50) * 50 / 50
    elif pm10 <= 250:
        return 100 + (pm10 - 100) * 100 / 150
    elif pm10 <= 350:
        return 200 + (pm10 - 250) * 100 / 100
    elif pm10 <= 430:
        return 300 + (pm10 - 350) * 200 / 80
    else:
        return 400 + (pm10 - 430) * 100 / 80

df['AQI_PM25'] = df['PM2.5'].apply(calculate_aqi_pm25)
df['AQI_PM10'] = df['PM10'].apply(calculate_aqi_pm10)
df['AQI'] = df[['AQI_PM25', 'AQI_PM10']].max(axis=1)

# AQI Category
def get_aqi_category(aqi):
    if pd.isna(aqi):
        return 'Unknown'
    elif aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Satisfactory'
    elif aqi <= 200:
        return 'Moderate'
    elif aqi <= 300:
        return 'Poor'
    elif aqi <= 400:
        return 'Very Poor'
    else:
        return 'Severe'

df['AQI_Category'] = df['AQI'].apply(get_aqi_category)

# 6️⃣ Seasonal Analysis
print("="*60)
print("SEASONAL ANALYSIS")
print("="*60)
seasonal_stats = df.groupby('Season').agg({
    'PM2.5': ['mean', 'min', 'max', 'std'],
    'PM10': ['mean', 'min', 'max', 'std'],
    'AQI': ['mean', 'min', 'max', 'std'],
    'Rainfall': 'sum',
    'Humidity': 'mean'
}).round(2)
print(seasonal_stats)

# 7️⃣ Monthly AQI Pattern
print("\n" + "="*60)
print("MONTHLY AQI PATTERN")
print("="*60)
monthly_aqi = df.groupby('Month')['AQI'].mean().round(2)
print(monthly_aqi)

# 8️⃣ Optional Visualizations
# Average AQI by Season
seasonal_aqi = df.groupby('Season')['AQI'].mean()
seasonal_aqi.plot(kind='bar', color='skyblue')
plt.title("Average AQI by Season")
plt.ylabel("AQI")
plt.show()

# Monthly AQI Trend
monthly_aqi.plot(marker='o')
plt.title("Monthly AQI Trend")
plt.xlabel("Month")
plt.ylabel("Average AQI")
plt.show()

# AQI Category Distribution
sns.countplot(x='AQI_Category', data=df)
plt.title("AQI Category Distribution")
plt.xticks(rotation=45)
plt.show()
