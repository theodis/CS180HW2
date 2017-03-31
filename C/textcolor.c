#include <stdio.h>
#include "textcolor.h"

void textcolor(int attr, int fg, int bg)
{ char command[13];
  sprintf(command, "%c[%d;%d;%dm", 0x1B, attr, fg + 30, bg + 40);
  printf("%s", command);
}
