# import pandas as pd
# import numpy as np

# # average_results_summary.csv 파일 로드
# average_results_df = pd.read_csv('average_results_summary.csv')

# # 오프셋과 스케일 계산 함수
# def calculate_offset_scale(mean, min_value, max_value, target_min, target_max):
#     offset = mean
#     scale = 1
#     if (max_value != min_value):
#         scale = (target_max - target_min) / (max_value - min_value)
#     return offset, scale

# # 잡음 공분산 계산 함수
# def calculate_covariance(data):
#     return np.cov(data, rowvar=False)

# # 결과 저장을 위한 리스트
# calibration_results = []

# # Acc_low 데이터 캘리브레이션
# for col in ['Acc_low_X', 'Acc_low_Y', 'Acc_low_Z']:
#     mean = average_results_df[f'{col}_mean'].values[0]
#     min_value = average_results_df[f'{col}_min'].values[0]
#     max_value = average_results_df[f'{col}_max'].values[0]
#     offset, scale = calculate_offset_scale(mean, min_value, max_value, -1.00, 1.00)
#     calibration_results.append({'Sensor': col, 'Offset': offset, 'Scale': scale})

# # Gyro_low 데이터 캘리브레이션
# for col in ['Gyro_low_X', 'Gyro_low_Y', 'Gyro_low_Z']:
#     mean = average_results_df[f'{col}_mean'].values[0]
#     offset = mean
#     calibration_results.append({'Sensor': col, 'Offset': offset, 'Scale': 1.0})

# # Acc 데이터 캘리브레이션
# for col in ['Acc_X', 'Acc_Y', 'Acc_Z']:
#     mean = average_results_df[f'{col}_mean'].values[0]
#     min_value = average_results_df[f'{col}_min'].values[0]
#     max_value = average_results_df[f'{col}_max'].values[0]
#     offset, scale = calculate_offset_scale(mean, min_value, max_value, -180.0, 180.0)
#     data = average_results_df[[f'{col}_mean', f'{col}_variance', f'{col}_max', f'{col}_min']].values
#     covariance = calculate_covariance(data)
#     calibration_results.append({'Sensor': col, 'Offset': offset, 'Scale': scale, 'Covariance': covariance})

# # Gyro 데이터 캘리브레이션
# for col in ['Gyro_X', 'Gyro_Y', 'Gyro_Z']:
#     mean = average_results_df[f'{col}_mean'].values[0]
#     min_value = average_results_df[f'{col}_min'].values[0]
#     max_value = average_results_df[f'{col}_max'].values[0]
#     offset, scale = calculate_offset_scale(mean, min_value, max_value, -180.0, 180.0)
#     data = average_results_df[[f'{col}_mean', f'{col}_variance', f'{col}_max', f'{col}_min']].values
#     covariance = calculate_covariance(data)
#     calibration_results.append({'Sensor': col, 'Offset': offset, 'Scale': scale, 'Covariance': covariance})

# # 결과를 데이터프레임으로 변환
# calibration_results_df = pd.DataFrame(calibration_results)

# # 결과를 CSV 파일로 저장
# calibration_results_df.to_csv('calibration_results.csv', index=False)


import pandas as pd
import numpy as np

# 평균 결과 파일 로드
average_results_df = pd.read_csv('average_results_summary.csv')

# 캘리브레이션 결과 저장을 위한 딕셔너리
calibration_results = {}

# Acc_low로 시작하는 가속도 센서 데이터의 오프셋과 스케일 계산
for axis in ['X', 'Y', 'Z']:
    mean_value = average_results_df[f'Acc_low_{axis}_mean'].values[0]
    variance_value = average_results_df[f'Acc_low_{axis}_variance'].values[0]
    
    # 오프셋 계산 (중간값이 0이 되도록)
    offset = mean_value
    
    # 스케일 계산 (1.00 ~ -1.00 사이의 값으로 조정)
    max_value = average_results_df[f'Acc_low_{axis}_max'].values[0]
    min_value = average_results_df[f'Acc_low_{axis}_min'].values[0]
    scale = 2.0 / (max_value - min_value)
    
    # 잡음 공분산 (칼만 필터에 적용)
    noise_covariance = variance_value
    
    calibration_results[f'Acc_low_{axis}'] = {
        'offset': offset,
        'scale': scale,
        'noise_covariance': noise_covariance
    }

# Gyro_low로 시작하는 자이로 센서 데이터의 오프셋과 잡음 공분산 계산
for axis in ['X', 'Y', 'Z']:
    mean_value = average_results_df[f'Gyro_low_{axis}_mean'].values[0]
    variance_value = average_results_df[f'Gyro_low_{axis}_variance'].values[0]
    
    # 오프셋 계산 (중간값이 0이 되도록)
    offset = mean_value
    
    # 잡음 공분산 (칼만 필터에 적용)
    noise_covariance = variance_value
    
    calibration_results[f'Gyro_low_{axis}'] = {
        'offset': offset,
        'noise_covariance': noise_covariance
    }

# Acc로 시작하는 가속도 센서 데이터의 스케일과 오프셋 계산
for axis in ['X', 'Y', 'Z']:
    mean_value = average_results_df[f'Acc_{axis}_mean'].values[0]
    variance_value = average_results_df[f'Acc_{axis}_variance'].values[0]
    
    # 오프셋 계산
    offset = mean_value
    
    # 스케일 계산 (degree 단위에 맞춤)
    max_value = average_results_df[f'Acc_{axis}_max'].values[0]
    min_value = average_results_df[f'Acc_{axis}_min'].values[0]
    
    scale = 1
    if (max_value != min_value):
        scale = 360.0 / (max_value - min_value)
    
    # 잡음 공분산 (칼만 필터에 적용)
    noise_covariance = variance_value
    
    calibration_results[f'Acc_{axis}'] = {
        'offset': offset,
        'scale': scale,
        'noise_covariance': noise_covariance
    }

# Gyro로 시작하는 자이로 센서 데이터의 스케일과 오프셋 계산
for axis in ['X', 'Y', 'Z']:
    mean_value = average_results_df[f'Gyro_{axis}_mean'].values[0]
    variance_value = average_results_df[f'Gyro_{axis}_variance'].values[0]
    
    # 오프셋 계산
    offset = mean_value
    
    # 스케일 계산 (degree 단위에 맞춤)
    max_value = average_results_df[f'Gyro_{axis}_max'].values[0]
    min_value = average_results_df[f'Gyro_{axis}_min'].values[0]
    scale = 360.0 / (max_value - min_value)
    
    # 잡음 공분산 (칼만 필터에 적용)
    noise_covariance = variance_value
    
    calibration_results[f'Gyro_{axis}'] = {
        'offset': offset,
        'scale': scale,
        'noise_covariance': noise_covariance
    }

# 캘리브레이션 결과를 CSV 파일로 저장
calibration_df = pd.DataFrame(calibration_results).T
calibration_df.to_csv('calibration_results.csv', index=True)
