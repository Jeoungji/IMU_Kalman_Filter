import pandas as pd
import matplotlib.pyplot as plt

folder = 'accel_angle_scale_calibration/'

# CSV 파일들을 읽어들입니다.
df1 = pd.read_csv(folder+'imu_data_non_calibration_90.csv')
df2 = pd.read_csv(folder+'imu_data_non_calibration_-90.csv')

# 각 파일의 Acc_Roll 평균을 계산합니다.
acc_roll_mean_1 = df1['Acc_Roll'].mean()
acc_roll_mean_2 = df2['Acc_Roll'].mean()

# 그래프 그리기 - 첫 번째 파일
plt.figure(figsize=(10, 6))

# 첫 번째 파일의 Acc_Roll 값 플로팅
plt.plot(df1['Acc_Roll'], label='File 1 Acc_Roll', linestyle='-')

# 첫 번째 파일의 Acc_Roll 평균 표시
plt.axhline(y=acc_roll_mean_1, color='blue', linestyle='--', label='File 1 Mean')

# 목표값 0 표시
plt.axhline(y=90, color='black', linestyle='-', label='Target Value (0)')

print("90:", acc_roll_mean_1)
plt.xlabel('Index')
plt.ylabel('Acc_Roll')
plt.title('Acc_Roll Values and Averages - File 1')
plt.legend()

# 그래프 저장 - 첫 번째 파일
plt.savefig(folder+'acc_roll_graph_file1.png')

# 그래프 출력 - 첫 번째 파일
plt.show()

# 그래프 그리기 - 두 번째 파일
plt.figure(figsize=(10, 6))

# 두 번째 파일의 Acc_Roll 값 플로팅
plt.plot(df2['Acc_Roll'], label='File 2 Acc_Roll', linestyle='-')

# 두 번째 파일의 Acc_Roll 평균 표시
plt.axhline(y=acc_roll_mean_2, color='orange', linestyle='--', label='File 2 Mean')

# 목표값 0 표시
plt.axhline(y=-90, color='black', linestyle='-', label='Target Value (0)')

print("-90:", acc_roll_mean_2)
plt.xlabel('Index')
plt.ylabel('Acc_Roll')
plt.title('Acc_Roll Values and Averages - File 2')
plt.legend()

# 그래프 저장 - 두 번째 파일
plt.savefig(folder+'acc_roll_graph_file2.png')

# 그래프 출력 - 두 번째 파일
plt.show()


# 90: 84.26783945617676
# -90: -89.92471615142823