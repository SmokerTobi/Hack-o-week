import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv('IIoT_Smart_Parking_Management.csv')

# Pre-processing: Convert timestamp to datetime and handle missing values
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.sort_values('Timestamp', inplace=True)
df['Sensor_Reading_Proximity'].fillna(method='ffill', inplace=True)

# Compute average proximity
avg_proximity = df['Sensor_Reading_Proximity'].mean()
print(f"Global Average Proximity: {avg_proximity:.2f} units")

# Plotting the distance trends
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Sensor_Reading_Proximity'], color='teal', linewidth=1, label='Proximity Reading')
plt.axhline(y=avg_proximity, color='red', linestyle='--', label=f'Average ({avg_proximity:.2f})')

plt.title('Time-Series Proximity Trends - Smart Parking')
plt.xlabel('Time')
plt.ylabel('Distance (Proximity Sensor)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('parking_proximity_trend.png')
