// 内存和 CPU 放在同一个结构体中，但在真实的硬件中，这两部分是分开的。
// CPU 和内存通过总线（bus）进行数据交换
//  [CPU]    [Memory]
//    |         |
// <===================> Memory Bus(proprietart)
//         |
//
pub struct Cpu {
  pub regs: [u64; 32],
  pub pc  :  u64,
  pub bus :  Bus,
}

// CPU 将会从 DRAM_BASE 处开始执行
impl Cpu {
  pub fn new(code: Vec<u8>) -> Self {
    let mut regs = [0; 32];
    //
    regs[2] = DRAM_END;
    let bus = Bus::new(code);
    Self{regs, pc: DRAM_BASE, bus}
  }

  /// Load a value from a dram
  pub fn load(&mut self, addr: u64, size: u64) -> Result<u64, Exception> {
    self.bus.load(addr, size)
  }

  /// Store a value to a dram
  pub fn store(&mut self, addr: u64, size: u64, value: u64) -> Result<u64, Exception> {
    self.buf.store(addr, size, value)
  }

  ///Get an instruction form the dram
  pub fn fetch(&mut self) -> Result<u64, Exception> {
    self.bus.load(self.pc, 32)
  }

  pub fn execute(&mut self, inst: u64) -> Result<u64, Exception> {
    
  }

}