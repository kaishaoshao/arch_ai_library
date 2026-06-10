# RISCV Simulator Memory Module

import os

mem = {
  'mem'  : None, # 内存数据
  'base' : 0,    # 起始地址
  'size' : 0,    # 内存大小
}


'''
Load data form memory
@param mem: memory dictionary
@param addr: address to load form
@param size: size in bytes to load
@return: loaded data as integer
'''
def mem_load(mem, addr, size):
  addr = addr - mem['base']
  # 从内存中读取指定大小的数据，并转换为整数返回
  return int.from_bytes(bytes(mem['mem'][addr:addr + size]), 'little')

'''
Store data to memory
@param mem: memory dictionary
@param addr: address to load form
@param size: size in bytes to load
@param value: data to store
'''
def mem_store(mem, addr, size, value):
  addr = addr - mem['base']   # 计算偏移地址
  for i in range(size):       # 按照字节存储数据
    mem['mem'][addr + i] = value & 0xFF # 存储最低字节
    value >>= 8                         # 右移8位，准备存储下一个字节

'''

'''
def check_addr(mem, addr):
  print(addr, addr - mem['base'], mem['size'])  # 调试信息

  # 检查地址是否在内存范围内
  if addr < 0 or (addr - mem['base'] >= mem['size']):
    return False
  else:
    return True

def load_image(mem, file, base = mem['base']):
  f = open(file, 'rb')
  size = os.path.getsize(file)  # 文件大小
  buf = f.read(size)            # 读取文件内容到缓冲区
  f.close()

  mem['mem'] = [i for i in buf] # 将缓冲区内容转换为字节列表
  mem['base'] = base            # 设置内存起始地址
  mem['size'] = size            # 设置内存大小

'''
测试代码
'''
# mem['mem'] = [1,2,3,4,5,6,7,8]
# print(hex(mem_load(mem, 4, 4)))
# hex(mem_load(mem, 0, 4))
# mem_store(mem, 0, 4, 0x01020304)
# print(hex(mem_load(mem, 0, 4)))

# riscv-none-elf-gcc -Ttest=0x80000000 -mno-relax -march=rv32i_zisr -nostdlib -ffreestanding
# -o test test0.S
# riscv-none-elf-objcopy -O binary test test.bin
# riscv-none-elf-objdump -D test
# load_image(mem, 'test.bin', 0x80000000)
