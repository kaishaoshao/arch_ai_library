import triton
import triton.language as tl
import torch

from display import print_end_line

@triton.jit
def demo3(z_ptr):
    range = tl.arange(0, 8)
    z = tl.store(z_ptr + range, 10, range < 5)

def run_demo3():
    print("Running demo3...")
    z = torch.ones(4,3)
    demo3[(1, 1, 1)](z)
    print(z)
    print_end_line()

if __name__ == "__main__":
    run_demo3()
    print_end_line()

