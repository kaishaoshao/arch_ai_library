import triton 
import triton.language as tl

@triton.jit
def add_kernel(x_ptr, # 指向第一个输入向量的指针
               y_ptr, # 指向第二个输入向量的指针
               output_ptr, # 指向输出向量的指针
               N_elements, # 向量的大小
               BLOCK_SIZE: tl.constexpr, # 每个程序处理元素的数量(每个线程块的大小
              ):
    # 有多个程序处理不同的数据
    pid = tl.program_id(axis=0) # 使用1D启动网格，因此轴为0
    # 该程序将处理相对初始数据偏移的输入
    # 如果有一个长度256，块为64的向量，那么有4个程序各自访问[0:64,64:128,128:192,192:256]
    # offset为指针列表
    block_start = pid * BLOCK_SIZE
    offset = block_start + tl.arange(0, BLOCK_SIZE)
    # 创建掩码以防止内存操作超出边界访问
    mask = offset < N_elements
    # 从DRAM 加载 x 和 y,如果输入不是块大小的整数倍，则屏蔽任何多余的元素
    x = tl.load(x_ptr + offset, mask=mask)
    y = tl.load(y_ptr + offset, mask=mask)
    # Write x + y 到 DRAM
    tl.store(output_ptr + offset, x + y, mask=mask)

