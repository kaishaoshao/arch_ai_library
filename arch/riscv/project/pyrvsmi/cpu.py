# 指令执行或外设中断都可能改写cpu中pc、regs、csr以及trap、trap_val的内容
from pyrvsmi.memory import mem_load
import logging

cpu = {
  'pc'       : 0,    #  程序计数器（0x800000000）
  'regs'     : [0 for _ in range(32)],   # 32个通用寄存器
  'csr'      : [0 for _ in range(4096)], # 4096个控制状态寄存器
  'trap'     : 0,                        # 异常标志
  'trap_val' : 0,                        # 异常值
}

'''
获取程序计数器
'''
def get_pc(cpu):
  return cpu['pc']

def set_pc(cpu, value):
  cpu['pc'] = value


'''
pc加4
'''
def pc_inc4(cpu):
  set_pc(cpu, get_pc(cpu) + 4)

'''
取指令
'''
def fetch(cpu, mem):
  pc = get_pc(cpu)
  return mem_load(mem, pc, 4)

'''
执行指令
'''
def execute(cpu, mem, inst):
  pc_inc4(cpu)

'''
单步执行
'''
def step(cpu, mem):
  inst = fetch(cpu, mem)
  #显示指令地址，指令的16进制和二进制编码
  log(f'{hex(cpu['pc']):<{10}}: {hex(inst):<{10}} --- {bin(inst):{36}}')
  execute(cpu, mem, inst)

def run(cpu, mem, image_filem, image_base=0x8000_0000, start=0x8000_0000):
  load_image(mem, image_file, image_base)
  set_pc(cpu, start)

