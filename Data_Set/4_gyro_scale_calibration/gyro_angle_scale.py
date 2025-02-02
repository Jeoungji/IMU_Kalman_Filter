import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load data
data_1 = pd.read_csv('imu_data_non_calibration_-90to90.csv')
data_2 = pd.read_csv('imu_data_non_calibration_90to-90.csv')

# Reverse data except for the 'Time' column
data_2_reversed = data_2.copy()
data_2_reversed.iloc[:, 1:] = data_2_reversed.iloc[:, 1:][::-1].reset_index(drop=True)

# Extract necessary columns
def extract_columns(data):
    return data['Time'], data['Roll_angle'], data['Acc_Roll'], data['Gyro_Roll']

time_1, roll_angle_1, acc_roll_1, gyro_roll_1 = extract_columns(data_1)
time_2, roll_angle_2, acc_roll_2, gyro_roll_2 = extract_columns(data_2_reversed)

# Calculate linear regression
def linear_regression(time, values):
    slope, intercept, _, _, _ = linregress(time, values)
    return slope, intercept

slope_roll_1, intercept_roll_1 = linear_regression(time_1, roll_angle_1)
slope_acc_1, intercept_acc_1 = linear_regression(time_1, acc_roll_1)
slope_gyro_1, intercept_gyro_1 = linear_regression(time_1, gyro_roll_1)

slope_roll_2, intercept_roll_2 = linear_regression(time_2, roll_angle_2)
slope_acc_2, intercept_acc_2 = linear_regression(time_2, acc_roll_2)
slope_gyro_2, intercept_gyro_2 = linear_regression(time_2, gyro_roll_2)

# Calculate scale values
scale_acc_1 = slope_roll_1 / slope_acc_1
scale_gyro_1 = slope_roll_1 / slope_gyro_1
scale_acc_2 = slope_roll_2 / slope_acc_2
scale_gyro_2 = slope_roll_2 / slope_gyro_2

# Plot linear approximation graphs and save automatically
plt.figure(figsize=(12, 12))

plt.subplot(3, 2, 1)
plt.plot(time_1, roll_angle_1, label='Roll_angle')
plt.plot(time_1, slope_roll_1 * time_1 + intercept_roll_1, 'r', label='Linear Approximation')
plt.title('Roll_angle (-90 to 90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(time_2, roll_angle_2, label='Roll_angle')
plt.plot(time_2, slope_roll_2 * time_2 + intercept_roll_2, 'r', label='Linear Approximation')
plt.title('Roll_angle (90 to -90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(time_1, acc_roll_1, label='Acc_Roll')
plt.plot(time_1, slope_acc_1 * time_1 + intercept_acc_1, 'r', label='Linear Approximation')
plt.title('Acc_Roll (-90 to 90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.subplot(3, 2, 4)
plt.plot(time_2, acc_roll_2, label='Acc_Roll')
plt.plot(time_2, slope_acc_2 * time_2 + intercept_acc_2, 'r', label='Linear Approximation')
plt.title('Acc_Roll (90 to -90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.subplot(3, 2, 5)
plt.plot(time_1, gyro_roll_1, label='Gyro_Roll')
plt.plot(time_1, slope_gyro_1 * time_1 + intercept_gyro_1, 'r', label='Linear Approximation')
plt.title('Gyro_Roll (-90 to 90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.subplot(3, 2, 6)
plt.plot(time_2, gyro_roll_2, label='Gyro_Roll')
plt.plot(time_2, slope_gyro_2 * time_2 + intercept_gyro_2, 'r', label='Linear Approximation')
plt.title('Gyro_Roll (90 to -90)')
plt.xlabel('Time (ms)')
plt.ylabel('Angle')
plt.legend()

plt.tight_layout()
plt.savefig('linear_approximation.png')  # Save the plot image automatically
plt.show()

# Save slopes, intercepts, and scales to a DataFrame
params = pd.DataFrame({
    'Parameter': ['Roll_angle_1', 'Acc_Roll_1', 'Gyro_Roll_1', 'Roll_angle_2', 'Acc_Roll_2', 'Gyro_Roll_2'],
    'Slope': [slope_roll_1, slope_acc_1, slope_gyro_1, slope_roll_2, slope_acc_2, slope_gyro_2],
    'Bias': [intercept_roll_1, intercept_acc_1, intercept_gyro_1, intercept_roll_2, intercept_acc_2, intercept_gyro_2],
    'Scale_to_Roll_angle': [None, scale_acc_1, scale_gyro_1, None, scale_acc_2, scale_gyro_2]
})

# Save to CSV file
params.to_csv('linear_approximation_params.csv', index=False)
