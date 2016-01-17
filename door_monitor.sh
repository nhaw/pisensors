#!/bin/bash

# Read from GP4.
# Note that GPIO pin '4' in the rpi breakout (broadcom numbering) is wpi number 7. See 'gpio readall' for mappings
gpio mode 7 in
gpio mode 7 up
while [ 1 ]; do
    gpio read 7
    sleep 0.5
done;
