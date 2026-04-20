import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Simulated hourly data (0–24 hours)
hours = np.arange(0, 24, 1)

# Simulate NO2 and CO concentrations with rush-hour peaks
NO2 = 40 + 100 * np.exp(-0.5 * ((hours - 8) / 2) ** 2) + 80 * np.exp(-0.5 * ((hours - 19) / 2) ** 2)
CO = 1 + 1.5 * np.exp(-0.5 * ((hours - 9) / 2.5) ** 2) + 1.2 * np.exp(-0.5 * ((hours - 20) / 2.5) ** 2)

# Create figure and dual-axis plot
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# Plot NO2 and CO lines
ax1.plot(hours, NO2, color='red', linewidth=2, label='NO₂ (µg/m³)')
ax2.plot(hours, CO, color='blue', linewidth=2, label='CO (mg/m³)')

# Shade rush-hour zones
ax1.axvspan(6, 10, color='gray', alpha=0.2)
ax1.axvspan(18, 22, color='gray', alpha=0.2)

# Labels and titles
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('NO₂ (µg/m³)', color='red')
ax2.set_ylabel('CO (mg/m³)', color='blue')
plt.title('Hourly Pollution Patterns in Delhi NCR\nTraffic-Related Air Pollution Levels')

# Customize ticks and grid
ax1.set_xticks(np.arange(0, 25, 2))
ax1.grid(True, linestyle='--', alpha=0.6)

# Legend
legend_elements = [
    Patch(facecolor='gray', alpha=0.2, label='Rush Hours'),
    Patch(facecolor='red', label='NO₂'),
    Patch(facecolor='blue', label='CO')
]
plt.legend(handles=legend_elements, loc='upper right')

# Save and show
plt.tight_layout()
plt.savefig('hourly_pollution_pattern.png', dpi=300)
plt.show()
