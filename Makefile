all: pwm_speaker_test

pwm_speaker_test: pwm_speaker_test.c
	gcc pwm_speaker_test.c -o pwm_speaker_test -lwiringPi
