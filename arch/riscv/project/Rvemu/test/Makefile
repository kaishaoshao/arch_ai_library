CC=zcc
CFLAGS=-nostdlib -mno-relax --target=riscv64 -march=rv64g
LKFLAGS=-Wl,-Ttext=0x0

OBJDCOPY=llvm-objcopy
OBJFORMAT=-O binary

add-addi.bin : add-addi.S
	${CC} ${CFLAGS} ${LKFLAGS} -o add-addi add-addi.S
	${OBJDCOPY} ${OBJFORMAT} add-addi add-addi.bin

clean:
	rm add-addi add-addi.bin -f