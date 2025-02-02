import pandas as pd
import matplotlib.pyplot as plt

# Load the data
imu_data = pd.read_csv('imu_data_non_calibration_all_sin.csv')

# Plot Acceleration sensor values over time
plt.figure(figsize=(10, 6))
plt.plot(imu_data['Time'], imu_data['Acc_low_X'], label='Acc_low_X')
plt.plot(imu_data['Time'], imu_data['Acc_low_Y'], label='Acc_low_Y')
plt.plot(imu_data['Time'], imu_data['Acc_low_Z'], label='Acc_low_Z')
plt.xlabel('Time (ms)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Acceleration Sensor Values Over Time')
plt.legend()
plt.grid(True)
plt.savefig('acceleration_sensor_values_over_time.png')
plt.close()

# Plot Gyroscope sensor values over time
plt.figure(figsize=(10, 6))
plt.plot(imu_data['Time'], imu_data['Gyro_low_X'], label='Gyro_low_X')
plt.plot(imu_data['Time'], imu_data['Gyro_low_Y'], label='Gyro_low_Y')
plt.plot(imu_data['Time'], imu_data['Gyro_low_Z'], label='Gyro_low_Z')
plt.xlabel('Time (ms)')
plt.ylabel('Gyroscope (deg/s)')
plt.title('Gyroscope Sensor Values Over Time')
plt.legend()
plt.grid(True)
plt.savefig('gyroscope_sensor_values_over_time.png')
plt.close()

# Plot angles over time
plt.figure(figsize=(10, 6))
plt.plot(imu_data['Time'], imu_data['Roll_angle'], label='Roll_angle (Motor)')
plt.plot(imu_data['Time'], imu_data['Acc_Roll'], label='Acc_Roll')
plt.plot(imu_data['Time'], imu_data['Gyro_Roll'], label='Gyro_Roll')
plt.plot(imu_data['Time'], imu_data['Kalman_Roll'], label='Kalman_Roll')
plt.xlabel('Time (ms)')
plt.ylabel('Angle (degrees)')
plt.title('Angles Over Time')
plt.legend()
plt.grid(True)
plt.savefig('angles_over_time.png')
plt.close()
