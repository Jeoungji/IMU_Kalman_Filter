import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from sklearn.linear_model import LinearRegression

# CSV 파일에서 데이터 로드
df = pd.read_csv('D:\BackUp\보고서\_4학년_1학기\ER\imu_data_x+.csv')

# 각 센서 데이터의 통계적 특성 계산
def calculate_statistics(data):
    mean = np.mean(data)
    variance = np.var(data)
    max_value = np.max(data)
    min_value = np.min(data)
    return mean, variance, max_value, min_value

# FFT 계산
def calculate_fft(data):
    data = np.asarray(data)  # numpy 배열로 변환
    N = len(data)
    T = (df['Time'].iloc[-1] - df['Time'].iloc[0]) / 1000  # total time in seconds
    fft_values = fft(data)
    fft_freq = np.fft.fftfreq(N, T / N)
    positive_freq_indices = np.where(fft_freq >= 0)  # 음수 주파수 성분 제거
    return fft_freq[positive_freq_indices], np.abs(fft_values[positive_freq_indices])

# 1차 함수 근사
def linear_approximation(x, y):
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    return model.coef_[0], model.intercept_

# 통계적 특성 계산
statistics = {}
for col in ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    statistics[col] = calculate_statistics(df[col])
    print(f"{col} - Average: {statistics[col][0]}, Dispersion: {statistics[col][1]}, Maximum: {statistics[col][2]}, Minimum: {statistics[col][3]}")

# FFT 계산
fft_results = {}
for col in ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    fft_freq, fft_magnitude = calculate_fft(df[col])
    fft_results[col] = (fft_freq, fft_magnitude)

# 1차 함수 근사
linear_models = {}
for col in ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    slope, intercept = linear_approximation(df['Time'].values, df[col].values)
    linear_models[col] = (slope, intercept)
    print(f"{col} - First-order approximation: y = {slope:.4f}x + {intercept:.4f}")

# 그래프 그리기
def plot_data_with_statistics(col):
    x = df['Time'].values
    y = df[col].values
    mean, variance, max_value, min_value = statistics[col]
    slope, intercept = linear_models[col]

    plt.figure(figsize=(12, 6))

    # 원본 데이터
    plt.plot(x, y, label=f'{col}', alpha=0.6)
    
    # 통계적 특성
    plt.axhline(y=mean, color='r', linestyle='--', label=f'Average: {mean:.2f}')
    plt.axhline(y=max_value, color='g', linestyle='--', label=f'Maximum: {max_value:.2f}')
    plt.axhline(y=min_value, color='b', linestyle='--', label=f'Minimum: {min_value:.2f}')

    # 1차 함수 근사
    plt.plot(x, slope * x + intercept, color='m', linestyle='--', label=f'First-order approximation: y = {slope:.4f}x + {intercept:.4f}')
    
    plt.xlabel('Time (ms)')
    plt.ylabel(col)
    plt.legend()
    plt.title(f'{col} Data and Statistical Properties')
    plt.show()

# FFT 그래프 그리기
def plot_fft(col):
    fft_freq, fft_magnitude = fft_results[col]

    plt.figure(figsize=(12, 6))
    plt.plot(fft_freq, fft_magnitude, label=f'{col} FFT')
    
    plt.yscale('log')  # y축을 로그 스케일로 설정
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.title(f'{col} FFT (log scale)')
    plt.show()

# 각 센서 데이터에 대해 그래프 출력
for col in ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
    plot_data_with_statistics(col)
    plot_fft(col)
