#!/bin/bash


control_c() { 
    gpio pwm 1 0
    exit 1
}

trap control_c SIGINT

# pwmFrequency in Hz = 19.2e6 Hz / pwmClock / pwmRange

# Note that for range 0-200, clock divisors 54 seem to be the loudest

# Enable gpio18 (pwm1???)
gpio mode 1 pwm
gpio pwm 1 0 # off (0 current through clock amp circuit)
gpio pwm-ms # mark:space mode. provides constant frequncy regardless of duty cycle (not the default for some reason)
gpio pwmc 48 # clock divisor
gpio pwmr 200 # range [0-200) represents duty cycle

sleep 1

gpio pwm 1 100 # 50% duty cycle  
while true; do
    for duty in `seq 110 10 170`; do
	echo $duty
  #gpio pwmc $div # clock divisor
	gpio pwm 1 $duty
	sleep `python -c "print $duty ** 6 / (3*(100**6))"`
    done
done;
sleep 1
gpio pwm 1 0 # off (0 current through clock amp circuit)
