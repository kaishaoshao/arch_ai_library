import torch
from torch import Tensor
import triton
import triton.language as tl

import jaxtyping
from jaxtyping import Float32, Int32

import triton_viz_test
from triton_viz_test import test

def add2_spec(x: Float32[200,]) -> Float32[200,]:
    return x + 10.0

def add_mask2_kernel(x_ptr, z_ptr, N0, B0: tl.constexpr):
    pid = tl.program_id(0)
    off_x = pid * B0 + tl.arange(0, B0)
    mask = off_x < N0
    x = tl.load(x_ptr + off_x, mask=mask)
    z = x + 10.0
    tl.store(z_ptr + off_x, z, mask=mask)
    return


test(add_mask2_kernel, add2_spec, nelem={"N0": 200}, viz=True)




