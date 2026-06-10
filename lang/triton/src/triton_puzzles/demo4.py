import triton
import triton.language as tl
import torch

from display import print_end_line

@triton.jit
def demo4(x_ptr):
    pid = tl.program_id(axis=0)
    range = tl.arange(0, 8) + pid * 8
    