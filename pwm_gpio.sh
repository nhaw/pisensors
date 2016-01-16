#!/bin/bash

# pwmFrequency in Hz = 19.2e6 Hz / pwmClock / pwmRange

# Note that for range 0-200, clock divisors 48-54 seem to be the loudest

# Enable gpio18 (pwm1???)
gpio mode 1 pwm
gpio pwm-ms # mark:space mode. provides constant frequncy regardless of duty cycle (not the default for some reason)
gpio pwmc 48 # clock divisor
gpio pwmr 200 # range [0-200) represents duty cycle
gpio pwm 1 100 # 50% duty cycle  
sleep 1
gpio pwm 1 0 # off (0 current through clock amp circuit)

sleep 1

gpio pwm 1 100 # 50% duty cycle  
for div in 24 28 32 36 40 44 48 54 60 66 72 78 74 80 90 100 150 200 250 300 350; do
  echo $div
  gpio pwmc $div # clock divisor
  sleep 1
done
gpio pwm 1 0 # off (0 current through clock amp circuit)
