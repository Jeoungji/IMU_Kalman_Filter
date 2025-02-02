import serial
import struct
import pandas as pd
from time import time

# 시리얼 포트 설정
ser = serial.Serial('COM34', 250000, timeout=1)
start_time = time()

data_list = []

ser.write(b'\xFF')
#ser.write(b'\x11')
success = False

try:
    while True:
        if not ser.readable():
            continue
        
        start = ser.read()
        if not (start == b'\xFF'):
            print("프레임 시작 바이트 누락 : " + str(start))
            ser.write(b'\xF0')
            exit()
            continue
            
        data = ser.read(48) # 나머지 데이터 읽기
        
        end = ser.read()
        if not (end == b'\xFF'):
            print("프레임 오류 : " + str(end))
            ser.write(b'\xF0')
            exit()
            continue
        unpacked_data = struct.unpack('<q f fff fff fff', data)
        #print(unpacked_data)
        # if (unpacked_data[1] > 90) or (unpacked_data[1] < -90):
        #     success = True
        #     break
        
        data_list.append(list(unpacked_data))
        
        if (len(data_list)%100 == 1):
            print("data : ", str(len(data_list)))#, "  ",len(data), "  ", data, "  ", unpacked_data)

        
        if (len(data_list) >= 5000): # 10초 이후에 종료
            success = True
            break
        
        

except KeyboardInterrupt:
    print("수동 종료")

finally:
    ser.write(b'\xF0')
    
    ser.close()
    print("수집된 데이터 개수: ", len(data_list))
    
    if (success):
        try:
            df = pd.DataFrame(data_list, columns=['Time', 
                                                  'Roll_angle',
                                                  'Acc_low_X', 'Acc_low_Y', 'Acc_low_Z', 
                                                  'Gyro_low_X', 'Gyro_low_Y', 'Gyro_low_Z',
                                                  'Acc_Roll', 'Gyro_Roll', 'Kalman_Roll'])
            print("데이터 프레임 생성 완료:")
            print(df.head())  # 데이터 프레임의 첫 몇 개의 행을 출력
        except Exception as e:
            print("데이터 프레임 생성 오류:", e)
        
        # CSV 파일 저장 확인
        try:
            df.to_csv('D:\BackUp\보고서\_4학년_1학기\ER\imu_data_non_calibration_all_sin.csv', index=False)
            print("CSV 파일 저장 완료")
        except Exception as e:
            print("CSV 파일 저장 오류:", e)