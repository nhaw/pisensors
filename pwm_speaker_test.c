#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main (void)
{
  printf ("Raspberry Pi wiringPi test program\n") ;

  if (wiringPiSetupGpio() == -1)
    exit (1) ;

  pinMode(18,PWM_OUTPUT);
  pwmWrite(18, 0); // off
  pwmSetMode(PWM_MODE_MS); // mark:space mode (constant freq)
  pwmSetClock(54);
  pwmSetRange(200);
  pwmWrite(18, 100); // 50% duty

  delay (500);

  pwmWrite(18, 0); // off
}
