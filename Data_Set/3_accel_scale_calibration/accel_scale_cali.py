import pandas as pd

# 데이터 로드
data1 = pd.read_csv('imu_data_non_calibration_0.csv')
data2 = pd.read_csv('imu_data_non_calibration_180.csv')
data3 = pd.read_csv('imu_data_non_calibration_90.csv')
data4 = pd.read_csv('imu_data_non_calibration_-90.csv')

# 각 데이터의 평균 계산
mean_values1 = data1.mean()
mean_values2 = data2.mean()
mean_values3 = data3.mean()
mean_values4 = data4.mean()

# Acc_low_Y와 Acc_low_Z의 평균 값 추출
acc_low_y_mean_0 = mean_values1['Acc_low_Y']
acc_low_y_mean_180 = mean_values2['Acc_low_Y']
acc_low_y_mean_90 = mean_values3['Acc_low_Y']
acc_low_y_mean_m90 = mean_values4['Acc_low_Y']

acc_low_z_mean_0 = mean_values1['Acc_low_Z']
acc_low_z_mean_180 = mean_values2['Acc_low_Z']
acc_low_z_mean_90 = mean_values3['Acc_low_Z']
acc_low_z_mean_m90 = mean_values4['Acc_low_Z']

# Acc_low_Y의 스케일 값 계산
acc_low_y_scale = 2 / (acc_low_y_mean_90 - acc_low_y_mean_m90)
# Acc_low_Z의 스케일 값 계산
acc_low_z_scale = 2 / (acc_low_z_mean_0 - acc_low_z_mean_180)

# 스케일 값을 데이터프레임으로 합치기
scale_df = pd.DataFrame({
    'Parameter': ['Acc_low_Y_scale', 'Acc_low_Z_scale'],
    'Scale': [acc_low_y_scale, acc_low_z_scale]
})

# 평균 값과 스케일 값을 하나의 데이터프레임으로 합치기
mean_df = pd.DataFrame({
    '0': mean_values1,
    '180': mean_values2,
    '90': mean_values3,
    '-90': mean_values4
})

# 평균 값과 스케일 값을 CSV 파일로 저장
mean_df.to_csv('mean_values.csv', index=True)
scale_df.to_csv('scale_values.csv', index=False)
