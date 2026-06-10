import triton
import triton.language as tl
import torch

import triton_viz

from display import print_end_line


"""
Demo1
这是一个关于内存加载操作的示例。它通过 arange在内存上创建序列。
默认情况下，PyTorch 张量的索引遵循列、行、深度或从右到左的顺序。
该操作还以掩码（mask）作为第二个参数，这在 Triton 中至关重要，
因为所有张量形状必须是 2 的幂次方。

Expected Results:

[0 1 2 3 4 5 6 7]
[1. 1. 1. 1. 1. 0. 0. 0.]


"""


@triton.jit
def demo1(x_ptr):
    # 使用 arange 创建一个整数序列
    range = tl.arange(0, 8)
    print(range)
    x = tl.load(x_ptr + range, range < 5, 0)  # 加载前五个元素
    print(x)

def run_demo1():
    print("Running demo1...")
    ms = triton.testing.do_bench(lambda: demo1[(1, 1, 1)](torch.ones(1, 7, device='cuda')))
    print(f"Time: {ms:.4f} ms")
    ts = triton.testing.do_bench(lambda: demo1[(1, 1, 1)](torch.ones(4, 3, device='cuda')))
    print(f"Time: {ts:.4f} ts")
    print_end_line()

# http://127.0.0.1:7860
def run_triton_viz():
    triton_viz.trace(demo1)[(1, 1, 1)](torch.ones(4, 3))
    triton_viz.launch(share=False)

if __name__ == "__main__":
    # run_demo1()
    run_triton_viz()
