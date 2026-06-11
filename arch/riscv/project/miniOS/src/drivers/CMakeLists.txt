add_library(miniOS-drivers STATIC)

target_sources(miniOS-drivers PRIVATE
  uart.c
)
