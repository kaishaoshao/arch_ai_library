#include "uart.h"

void kmain(void) {
  uart_init();
  uart_puts("Hello miniOS\n");
  return;
}