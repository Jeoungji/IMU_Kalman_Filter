import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 파일 리스트
file_list = ['imu_data_x+.csv', 'imu_data_x-.csv', 'imu_data_y+.csv', 'imu_data_y-.csv', 'imu_data_z+.csv', 'imu_data_z-.csv']

# 각 파일에서 데이터를 데이터프레임으로 로드
df_list = [pd.read_csv(file) for file in file_list]

# 각 센서 데이터에 대한 통계적 특성 계산
def calculate_statistics(data):
    mean = np.mean(data)
    variance = np.var(data)
    max_value = np.max(data)
    min_value = np.min(data)
    return mean, variance, max_value, min_value

# 1차 근사
def linear_approximation(x, y):
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    return model.coef_[0], model.intercept_

# 통계적 특성과 1차 근사 계산 및 저장
results = []
for df, filename in zip(df_list, file_list):
    file_results = {'Filename': filename}
    for col in ['Acc_low_X', 'Acc_low_Y', 'Acc_low_Z', 'Gyro_low_X', 'Gyro_low_Y', 'Gyro_low_Z', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Euler_X', 'Euler_Y', 'Euler_Z']:
        mean, variance, max_value, min_value = calculate_statistics(df[col])
        slope, intercept = linear_approximation(df['Time'].values, df[col].values)
        file_results[f'{col}_mean'] = mean
        file_results[f'{col}_variance'] = variance
        file_results[f'{col}_max'] = max_value
        file_results[f'{col}_min'] = min_value
        file_results[f'{col}_slope'] = slope
        file_results[f'{col}_intercept'] = intercept
    results.append(file_results)

# 결과를 데이터프레임으로 변환
results_df = pd.DataFrame(results)

# 결과를 CSV 파일로 저장
results_df.to_csv('results_summary.csv', index=False)

# 각 컬럼별로 평균 계산
average_results = {}
for col in ['Acc_low_X', 'Acc_low_Y', 'Acc_low_Z', 'Gyro_low_X', 'Gyro_low_Y', 'Gyro_low_Z', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Euler_X', 'Euler_Y', 'Euler_Z']:
    average_results[f'{col}_mean'] = results_df[[f'{col}_mean']].mean().values[0]
    average_results[f'{col}_variance'] = results_df[[f'{col}_variance']].mean().values[0]
    average_results[f'{col}_max'] = results_df[[f'{col}_max']].mean().values[0]
    average_results[f'{col}_min'] = results_df[[f'{col}_min']].mean().values[0]
    average_results[f'{col}_slope'] = results_df[[f'{col}_slope']].mean().values[0]
    average_results[f'{col}_intercept'] = results_df[[f'{col}_intercept']].mean().values[0]

# 평균 결과를 데이터프레임으로 변환
average_results_df = pd.DataFrame([average_results])

# 평균 결과를 CSV 파일로 저장
average_results_df.to_csv('average_results_summary.csv', index=False)

# 그래프를 그리고 저장
def plot_and_save(df, col, statistics, linear_model, filename):
    x = df['Time'].values
    y = df[col].values
    mean, variance, max_value, min_value = statistics
    slope, intercept = linear_model

    fig, ax = plt.subplots(figsize=(12, 6))

    # 원본 데이터와 통계적 특성 및 1차 근사
    ax.plot(x, y, label=f'{col}', alpha=0.6)
    ax.axhline(y=mean, color='r', linestyle='--', label=f'Average: {mean:.2f}')
    ax.axhline(y=max_value, color='g', linestyle='--', label=f'Maximum: {max_value:.2f}')
    ax.axhline(y=min_value, color='b', linestyle='--', label=f'Minimum: {min_value:.2f}')
    ax.plot(x, slope * x + intercept, color='m', linestyle='--', label=f'First-order approximation: y = {slope:.4f}x + {intercept:.4f}')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel(col)
    ax.legend()
    ax.set_title(f'{col} Data and Statistical Properties')

    plt.tight_layout()
    save_filename = f"{filename.split('.')[0]}_{col}.png"
    plt.savefig(save_filename)
    plt.close()

# 각 파일 및 각 컬럼에 대해 그래프를 그리고 저장
for df, filename in zip(df_list, file_list):
    for col in ['Acc_low_X', 'Acc_low_Y', 'Acc_low_Z', 'Gyro_low_X', 'Gyro_low_Y', 'Gyro_low_Z', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Euler_X', 'Euler_Y', 'Euler_Z']:
        statistics = (results_df.loc[results_df['Filename'] == filename, f'{col}_mean'].values[0],
                      results_df.loc[results_df['Filename'] == filename, f'{col}_variance'].values[0],
                      results_df.loc[results_df['Filename'] == filename, f'{col}_max'].values[0],
                      results_df.loc[results_df['Filename'] == filename, f'{col}_min'].values[0])
        linear_model = (results_df.loc[results_df['Filename'] == filename, f'{col}_slope'].values[0],
                        results_df.loc[results_df['Filename'] == filename, f'{col}_intercept'].values[0])
        plot_and_save(df, col, statistics, linear_model, filename)













