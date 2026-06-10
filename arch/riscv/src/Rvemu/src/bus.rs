// 总线是 CPU 与各种 IO 设备（如键盘、鼠标、屏幕等）通信的渠道。
// 总线上不同的地址范围对应了不同的设备。
// CPU 通过给总线发指令来间接操作其他的设备。
// 总线同样仅提供两个操作：store，load。
// CPU 现在不包含内存，但目前我们只有一个（DRAM）
pub struct Bus {
  dram: Dram,
}

impl Bus {
  pub fn new(code: Vec<u8> -> Bus) {
    Self {dram: Dram::new(code)}
  }

  pub fn load(&mut self, addr: u64, size: u64) -> Result<u64, Exception> {
    match addr {
      // addr >= DRAM_BASE && addr <= DRAM_END
      DRAM_BASE..=DRAM_END => self.dram.load(addr, size),
      // default:
      _ => Err(Exception::LoadAccessFault(addr)),
    }
  }

  pub fn store(&mut self, addr: u64, size: u64, value: u64) -> Result<(), Exception> {
    match addr {
      DRAM_BASE..=DRAM_END => self.dram.store(addr, size, value),
      _ => Err(Exception::StoreAMOAccessFault(addr));
    }
  }

}


