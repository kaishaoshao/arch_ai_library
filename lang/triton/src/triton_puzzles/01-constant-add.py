import torch
from torch import Tensor
import triton
import triton.language as tl

import jaxtyping
from jaxtyping import Float32, Int32

import triton_viz_test
from triton_viz_test import test


def add_spec(x: Float32[Tensor, "32"]) -> Float32[Tensor, "32"]:
    "This is the spec that you should implement. Uses typing to define sizes."
    return x + 10.

@triton.jit
def add_kernel(x_ptr, z_ptr, N0, B0: tl.constexpr):
    off_x = tl.arange(0, B0)
    x = tl.load(x_ptr + off_x)
    z = x + 10.0
    tl.store(z_ptr + off_x, z)
    return

test(add_kernel, add_spec, nelem={"N0": 128}, viz=True)









