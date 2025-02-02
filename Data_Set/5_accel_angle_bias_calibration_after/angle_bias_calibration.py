import pandas as pd
import matplotlib.pyplot as plt

folder = 'accel_angle_bias_calibration_after/'

# CSV 파일들을 읽어들입니다.
df1 = pd.read_csv(folder+'imu_data_non_calibration_0.csv')

# 각 파일의 Acc_Roll 평균을 계산합니다.
acc_roll_mean_1 = df1['Acc_Roll'].mean()

# 그래프 그리기
plt.figure(figsize=(10, 6))

# 각 파일의 Acc_Roll 값 플로팅
plt.plot(df1['Acc_Roll'], label='File 1 Acc_Roll', linestyle='-')

# 각 파일의 Acc_Roll 평균 표시
plt.axhline(y=acc_roll_mean_1, color='blue', linestyle='--', label='File 1 Mean')

# 목표값 0 표시
plt.axhline(y=0, color='black', linestyle='-', label='Target Value (0)')

plt.xlabel('Index')
plt.ylabel('Acc_Roll')
plt.title('Acc_Roll Values and Averages')
plt.legend()

print(acc_roll_mean_1)
# 그래프 저장
plt.savefig(folder+'acc_roll_graph.png')

# 그래프 출력
plt.show()
 #  0.006062790785495599
