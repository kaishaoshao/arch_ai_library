import triton
import triton.language as tl

import torch

from display import print_end_line

@triton.jit
def demo2(x_ptr):
    # 创建索引(0-7)形状[8,1]  索引(0,3)形状 [1,4]
    '''
    [:, None]将形状为 (8,)的一维数组转换为形状为 (8, 1)的二维数组（列向量）。例如：

    [0,        [[0],
     1,   =>    [1],
     2,         [2],
   ...]        ...]
    [None, :]将形状为 (4,)的一维数组转换为形状为 (1, 4)的二维数组（行向量）。例如：
    [0, 1, 2, 3]  =>  [[0, 1, 2, 3]]
    '''
    i_range = tl.arange(0, 8)[:, None]
    j_range = tl.arange(0, 4)[None, :]
    range = i_range * 4 + j_range
    print(range)
    x = tl.load(x_ptr + range, (i_range < 4) & (j_range < 3), 0)
    print(x)

def run_demo2():
    print("Running demo2...")
    demo2[(1,1,1)](torch.ones(4, 4))
    print_end_line()

if __name__ == "__main__":
    run_demo2()
    print_end_line()
