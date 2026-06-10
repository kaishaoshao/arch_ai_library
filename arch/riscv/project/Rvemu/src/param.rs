// 定义内存的大小来初始化 CPU
pub const DRAM_BASE：u64 = 0x8000_0000;
pub const DRAM_SIZE: u64 = 1024 * 1024 * 128;
pub const DRAM_END : u64 = DRAM_BASE + DRAM_SIZE;
