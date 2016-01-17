#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main (void)
{
  printf ("Raspberry Pi wiringPi test program\n") ;

  if (wiringPiSetupGpio() == -1)
    exit (1);

  const int GPIO4 = 4; // wiringPi actually gets these right here.. just not in the 'gpio' program

  pinMode(GPIO4,INPUT);
  pullUpDnControl(GPIO4,PUD_UP);

  int was_open = digitalRead(GPIO4);
  const char* states[2] = { "closed", "open" };
  const char* state = states[was_open];
  printf("Door currently %s\n", state);
  fflush(stdout);
  for (;;) {
    const int is_open = digitalRead(GPIO4);
    if (is_open != was_open) {
      printf("Door now %s\n", states[is_open]);
      fflush(stdout);
    }
    was_open = is_open;
    printf("%d\n",is_open);
    fflush(stdout);
    delay (500);
  }
}
