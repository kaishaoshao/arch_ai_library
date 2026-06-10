pub struct Dram {
  pub dram: Vec<u8>,
}

// 内存（DRAM）只有两个功能：store，load。
// 保存和读取的有效位数是 8，16，32，64。采用的是小端字节序。
// 计算机的内存模拟为一个巨大的 字节数组 (Vec<u8>)，
// 并提供了读 (load) 和写 (store) 两个接口来操作这块内存
// DRAM_BASE 其实地址在riscv中通常是
impl Dram {
  pub fn new(code: Vec<u8>) -> Dram {
    let mut dram = vec![0; DRAM_SIZE as usize];
    dram.splice(..code.len(), code.into_iter());
    Self{dram}
  }

  // addr/size must be valid, Check in bus
  pub fn load(&self, addr: u64, size: u64)-> Result<u64, Exception> {
    if ![8, 16, 32, 64].contains(&size) {
      return Err(LoadAccessFault(addr));
    }
    let nbytes = size / 8;
    let index = (addr - DRAM_BASE) as usize;
    // 从内存数组中取出第 1 个字节，把它变成 64 位的整数，作为基础值存起来
    let mut code = self.dram[index] as u64;
    // shift the bytes to build up desired value
    for i in 1..nbytes {
      code |= (self.dram[index + i as usize] as u64) << (i * 8);
    }
    return Ok(code);
  }

  pub fn store(&mut self, addr: u64, size: u64, value: u64) -> Result<(), Exception> {
    if ![8, 16, 32, 64].contains(&size) {
      return Err(StoreAMOAccessFault(addr));
    }
    let nbytes = size / 8;
    let index = (addr - DRAM_BASE) as usize;
    for i in 0..nbytes {
      let offset = 8 * i as usize;
      self.dram[index + i as usize] = ((value >> offset) & 0xff) as u8;
    }
    return Ok(());
  }

}