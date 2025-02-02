import pandas as pd
import matplotlib.pyplot as plt

folder = 'accel_angle_bias_calibration/'

# CSV 파일들을 읽어들입니다.
df1 = pd.read_csv(folder+'imu_data_non_calibration_0_1.csv')
df2 = pd.read_csv(folder+'imu_data_non_calibration_0_2.csv')
df3 = pd.read_csv(folder+'imu_data_non_calibration_0_3.csv')

# 데이터프레임들을 하나로 합칩니다.
combined_df = pd.concat([df1, df2, df3])

# 각 파일의 Acc_Roll 평균을 계산합니다.
acc_roll_mean_1 = df1['Acc_Roll'].mean()
acc_roll_mean_2 = df2['Acc_Roll'].mean()
acc_roll_mean_3 = df3['Acc_Roll'].mean()

# 전체 Acc_Roll 평균을 계산합니다.
acc_roll_mean_total = combined_df['Acc_Roll'].mean()

# 전체 Acc_Roll 평균 출력
print(f"전체 Acc_Roll 평균: {acc_roll_mean_total}")

# 그래프 그리기
plt.figure(figsize=(10, 6))

# 각 파일의 Acc_Roll 값 플로팅
plt.plot(df1['Acc_Roll'], label='File 1 Acc_Roll', linestyle='-')
plt.plot(df2['Acc_Roll'], label='File 2 Acc_Roll', linestyle='-')
plt.plot(df3['Acc_Roll'], label='File 3 Acc_Roll', linestyle='-')

# 각 파일의 Acc_Roll 평균 표시
plt.axhline(y=acc_roll_mean_1, color='blue', linestyle='--', label='File 1 Mean')
plt.axhline(y=acc_roll_mean_2, color='orange', linestyle='--', label='File 2 Mean')
plt.axhline(y=acc_roll_mean_3, color='green', linestyle='--', label='File 3 Mean')

# 전체 Acc_Roll 평균 표시
plt.axhline(y=acc_roll_mean_total, color='red', linestyle='-', label='Total Mean')

# 목표값 0 표시
plt.axhline(y=0, color='black', linestyle='-', label='Target Value (0)')

plt.xlabel('Index')
plt.ylabel('Acc_Roll')
plt.title('Acc_Roll Values and Averages')
plt.legend()

# 그래프 저장
plt.savefig(folder+'acc_roll_graph.png')

# 그래프 출력
plt.show()

 # 2.7927101144313813
