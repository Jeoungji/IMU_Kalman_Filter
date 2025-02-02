#include "MYMPU9250.h"
#include "Watchdog_t4.h"

#define SPI_CLOCK 5000000  // 8MHz clock works.
#define SS_PIN   37 

#define DIR 23
#define PULSE 22

WDT_T4<WDT1> wdt;
void myCallback() {
  Serial.println("FEED THE DOG SOON, OR RESET!");
}


unsigned long long start;
MYMPU9250 mpu(&SPI, SPI_CLOCK, SS_PIN);

void setup() {

  SerialUSB1.begin(250000); // 500kbps로 시리얼 통신 설정
  Serial.begin(250000);

  pinMode(DIR, OUTPUT);
  pinMode(PULSE, OUTPUT);

  WDT_timings_t config;
  config.trigger = 2;
  config.timeout = 4;
  config.callback = myCallback;
  wdt.begin(config);

	while(mpu.auto_init() > 0) {
    Serial.println("mpu set error");
    delay(5000);
  }
   // WAITFORINPUT();
  while(1) {
    wdt.feed();
    if (SerialUSB1.available()) {
      uint8_t a = SerialUSB1.read();
      if (a == 0xFF) break;
    }
    if (Serial.available()) {
      char b = Serial.read();
      if (b == 's') break;
    }
  }
  start = millis();
}

uint32_t motortime = 0;
uint32_t imutime = 0;

int goal = 0;
int mode = 0;
int current = 0;

void loop() {
  wdt.feed();
  if (Serial.available()) {
    char a = Serial.read();
    if (a == 'w') {
      goal = goal + (6400/4);
      mode = 0;
    }
    else if (a == 's') {
      goal = goal - (6400/4);
      mode = 0;
    }
    else if (a == 'x') {
      goal= 0;
      mode = 0;
    }
    else if (a == 'c') {
      if (goal == 0)
        current= 0;
      mode = 0;
    }
    else if (a == 'q') {
      mode = 1;
    }
  }
  if (SerialUSB1.available()) {
    uint8_t d = SerialUSB1.read();
    if (d == 0xF0) {
      mode = 0;
      goal = 0;
      //while(1) {}
    }
    else if (d == 0x10) {
      goal = 0;
    } 
    else if (d == 0x11) {
      goal = 6400/4;
    } 
    else if (d == 0x12) {
      goal = -6400/4;
    } 
  }
  
  if (millis() - imutime >= 5) {
    imutime = millis();
    mpu.CalKalmanAngle(millis());
    unsigned long long time = millis()- start;
    //Serial.printf("%f, %f, %f\n", mpu.accel_data[0], mpu.accel_data[1], mpu.accel_data[2]);
    // Serial.print( "  IMU : ");
    // Serial.print((mpu.accelangle.Pitch));
    // Serial.print( ", ");
    Serial.print((mpu.accelangle.Roll));
    // Serial.print( ", ");
    // Serial.print((mpu.accelangle.Yaw));
    // Serial.print( ",   ");
    // Serial.print((mpu.gyroangle.Pitch));
    Serial.print( ", ");
    Serial.print((mpu.gyroangle.Roll));
    // Serial.print( ", ");
    // Serial.print((mpu.gyroangle.Yaw));
    // Serial.print( ",   ");
    // Serial.print((mpu.KalmanAngle.Pitch));
    Serial.print( ", ");
    Serial.print((mpu.KalmanAngle.Roll));
    //Serial.print( ", ");
    // Serial.print((mpu.KalmanAngle.Yaw));
    
    // Serial.print((mpu.accel_lowdata[0]));
    // Serial.print( ", ");
    // Serial.print((mpu.accel_lowdata[1]));
    // Serial.print( ", ");
    // Serial.print((mpu.accel_lowdata[2]));
    Serial.print( ",  accel:");
    Serial.print((mpu.accel_data[0]));
    Serial.print( ", ");
    Serial.print((mpu.accel_data[1]));
    Serial.print( ", ");
    Serial.print((mpu.accel_data[2]));

    Serial.print( ",  gyro:");
    Serial.print((mpu.gyro_data[0]));
    Serial.print( ", ");
    Serial.print((mpu.gyro_data[1]));
    Serial.print( ", ");
    Serial.println((mpu.gyro_data[2]));
Serial.println("");

    unsigned char buf[50] = {0,};
    memset(buf,0xFF, 50);
    float real = (float)current / 6400 * 360;
    buf[0] = 0xFF;
    // 시간 데이터
    memcpy(buf+1, &time, 8);
    memcpy(buf+9, &real, 4);
    memcpy(buf+13, mpu.accel_data, 12);
    memcpy(buf+25, mpu.gyro_data, 12);
    memcpy(buf+37, &mpu.accelangle.Roll, 4);
    memcpy(buf+41, &mpu.gyroangle.Roll, 4);
    memcpy(buf+45, &mpu.KalmanAngle.Roll, 4);

    buf[49] = 0xFF;

    SerialUSB1.write(buf, 50);
  }

  if (mode == 0) {
    if (micros() - motortime >= 5000) {
      motortime = micros();
      
      
      if (current != goal) {
        digitalWriteFast(PULSE, HIGH);
        delayMicroseconds(10);
        digitalWriteFast(PULSE, LOW);
        if (current < goal) {
          digitalWriteFast(DIR, LOW);
          current ++;
        }
        else if (current > goal) {
          digitalWriteFast(DIR, HIGH);
          current --;
        }
      }
      Serial.printf("goal : %f, current : %f\n", (float)goal / 6400 * 360, (float)current / 6400 * 360);
    }
  }
  if (mode == 1) {
    float cmd = sin((float)millis()/1000.0*3.14/8) * 90.0;
    goal = (int)(6400 * ((float)cmd/360.0));
    if (goal > current ) {
    digitalWrite(DIR, LOW);
    digitalWrite(PULSE, HIGH);
    delayMicroseconds(5);
    digitalWrite(PULSE, LOW);
    current++;
    delayMicroseconds(200);
  }
  else if (goal < current ) {
    digitalWrite(DIR, HIGH);
    digitalWrite(PULSE, HIGH);
    delayMicroseconds(5);
    digitalWrite(PULSE, LOW);
    current--;
    delayMicroseconds(200);
  }
  }
}
