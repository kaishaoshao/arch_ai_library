.global _start

.data
x: .word 100
y: .word 200
z: .word 0
stack_end: .skip 1024

.text
_start:
  la sp, stack_start

  lw a0, x
  lw a1, y
  add a2, a1, a0

  sw a2, z, t0

  j _start
