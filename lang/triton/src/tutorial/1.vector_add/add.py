## 辅助函数
import torch
import triton
from add_kernel import add_kernel

def add(x: torch.Tensor, y: torch.Tensor):
    # 需要预分配输出
    output = torch.empty_like(x)
    assert x.is_cuda and y.is_cuda and output.is_cuda
    n_elements = output.numel()
    # SPMD 启动网格表示并运行的内核数量
    # 它类似于CUDA启动网络 可以是Tuplep[int],也可以是Callable(metaparameters) -> Tuple[int]
    # 在这种情况下，使用1D启动网格，其中大小是块的数量
    grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']), )

    add_kernel[grid](x, y, output, n_elements, block_size=1024)
    return output

