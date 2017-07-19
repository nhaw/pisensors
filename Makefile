all: pwm_speaker_test door_sensor_read_test imu

pwm_speaker_test: pwm_speaker_test.c
	gcc pwm_speaker_test.c -o pwm_speaker_test -lwiringPi

door_sensor_read_test: door_sensor_read_test.c
	gcc door_sensor_read_test.c -o door_sensor_read_test -lwiringPi

imu: imu.c
	gcc imu.c -o imu -lwiringPi
