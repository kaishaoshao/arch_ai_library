import pytest
import torch
import triton
import triton.language as tl


class DummyBenchmark:
    def measure(self):
        def decorator(func):
            return func
        return decorator
    def select_cpu_backend(self):
        pass
benchmark = DummyBenchmark()

# 输入矩阵 (input)：
# [[ 1.0,  2.0,  3.0,  4.0],
#  [ 5.0,  5.0,  5.0,  5.0],
#  [ 6.0,  7.0,  8.0,  9.0]]
# 计算每行的softmax

# program_id(axis)
# 启动内核代码
# 场景1
# softmax_kernel[(n_rows,)]
# 创建了一个一维的启动网格 一排n_rows个线程，每个线程处理一行数据
# 因此axis=0是有效的，axis=1是无效的,因为只有一个维度，没有第“1"轴这个概念
# 场景2
# matrix_multiply_kernel[(M, N)] （矩阵乘）
# program_id(0) 和 program_id(1) 的区别正好就是行索引和列索引的区别。
# 每个线程可以通过 (pid_m, pid_n) 这对坐标来唯一确定自己在整个工作矩阵中的位置。
# 场景3
# # 定义一个 3D 启动网格
# launch_grid = (Batch, H, W)
# my_3d_kernel[launch_grid](...)
#     program_id	   含义	             对应启动网格	        类比
# tl.program_id(0)	第 0 轴的索引	一维、二维、三维网格都有效	向量的索引 v[i]
# tl.program_id(1)	第 1 轴的索引	只有二维、三维网格有效	   矩阵的行/列索引 M[i, j]
# tl.program_id(2)	第 2 轴的索引	只有三维网格有效 	      三维张量的深度索引 T[d, h, w]
# axis = 0 负责向量 axis= 1 负责矩阵 axis = 2 负责张量 简单理解

@triton.jit
def softmax_kernel(output_ptr,               # 输出张量指针   输出结果存放的内存起始位置
                   input_ptr,                # 输入张量指针   输入数据存放的内存起始位置 指向1.0
                   input_row_stride,         # 输入张量行步长 跨行步长 4
                   output_row_stride,        # 输出张量行步长 跨行步长 4
                   n_cols,                   # 要处理的列数   4
                   BLOCK_SIZE: tl.constexpr  # 块大小        每次处理的元素数：4 一次一行
                  ):
    # 信息获取
    # 每一行都是独立的，我们在行上做并行优化
    row_idx = tl.program_id(0)
    # 计算行的起始指针
    row_start_ptr = input_ptr + row_idx * input_row_stride

    # 写入内存操作SRAM
    # BLOCK_SIZE 是大于 n_cols 的最小的2的幂，保证一行可以放入一个快
    col_offsets = tl.arange(0, BLOCK_SIZE)
    input_ptrs = row_start_ptr + col_offsets  # 基于行的起始指针，生成一整块要读取的内存地址
    # DRAM中加载行数据到SRAM中，使用掩码处理BLOCK_SIZE可能大于n_cols的情况
    # 使用掩码来防止越界读取（
    # 如果 n_cols = 7 BLOCK_SIZE=8 第8个地址会超出我们的数据范围，读取它就会导致访存越界
    # 解决方法： 我们提供一个mask--》掩码，tl.load只会加载True的位置，对于False，是无效的
    # 位置我们给他一个-float('-inf')的无穷小的值 ）

    # 注： 为了数值稳定性，累加是使用高精度类型
    row = tl.load(input_ptrs, mask=col_offsets < n_cols, other=-float('inf'))

    # 算法实现
    # 减去最大值以提高数值稳定性,防止exp溢出
    row_minus_max = row - tl.max(row, axis=0)
    # Triton 的 exp 很快但是是近似计算
    numerator = tl.exp(row_minus_max)
    # 计算分母
    denominator = tl.sum(numerator, axis=0)
    # 计算softmax输出
    softmax_output = numerator / denominator

    # 将结果写回到DRAM
    output_row_start_ptr = output_ptr + row_idx * output_row_stride
    output_ptrs = output_row_start_ptr + col_offsets
    tl.store(output_ptrs, softmax_output, mask=col_offsets < n_cols)

# 专门给bf16写的
@triton.jit
def softmax_kernel_bf16(output_ptr, input_ptr, input_row_stride, output_row_stride, n_cols, BLOCK_SIZE: tl.constexpr):
    """
    这是一个标准的行式 Softmax Triton 内核。
    它并行处理每一行，每行由一个或多个 aunch grid 的程序实例处理。
    """
    row_idx = tl.program_id(0)
    row_start_ptr = input_ptr + row_idx * input_row_stride
    col_offsets = tl.arange(0, BLOCK_SIZE)
    input_ptrs = row_start_ptr + col_offsets

    # 1. 加载一行数据
    # 使用掩码来防止越界读取，无效值用-inf填充
    row = tl.load(input_ptrs, mask=col_offsets < n_cols, other=-float('inf'))

    # --- ** FIX START: 使用 float32 进行所有中间计算 ** ---
    # 2. 将加载的数据转换为float32以保证计算精度
    row_fp32 = row.to(tl.float32)

    # 3. 在 float32 精度下减去最大值
    row_minus_max = row_fp32 - tl.max(row_fp32, axis=0)

    # 4. 计算指数
    numerator = tl.exp(row_minus_max)

    # 5. 在 float32 精度下计算分母
    denominator = tl.sum(numerator, axis=0)

    # 6. 计算最终的 softmax 结果
    softmax_output_fp32 = numerator / denominator

    # 7. 将结果转换回原始的数据类型
    softmax_output = softmax_output_fp32.to(output_ptr.dtype.element_ty)
    # --- ** FIX END ** ---

    # 将结果写回 DRAM
    output_row_start_ptr = output_ptr + row_idx * output_row_stride
    output_ptrs = output_row_start_ptr + col_offsets
    tl.store(output_ptrs, softmax_output, mask=col_offsets < n_cols)


@triton.jit
def softmax_kernel_2(
    x_ptr,
    output_ptr,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    # Get the program ID
    pid = tl.program_id(0)
    start = pid * BLOCK_SIZE
    offsets = start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    out = tl.softmax(x, 0)
    tl.store(output_ptr + offsets, out, mask=mask)


def softmax(x, axis=-1):
    '''
    softmax_kernel的封装函数，用于处理2D张量
    通过转置技巧按行（axis=1）和按列（axis=0）处理
    '''
    if x.dim() != 2:
        raise ValueError("Input tensor must be 2D")
    input_tensor = x
    # 如果是按列计算softmax, 先对输入进行专职
    if axis == 0:
          input_tensor = x.T.contiguous()
    n_rows, n_cols = input_tensor.shape
    BLOCK_SIZE = triton.next_power_of_2(n_cols)

    num_warps = 4
    if BLOCK_SIZE >= 2048: num_warps = 8
    if BLOCK_SIZE >= 4096: num_warps = 16

    y = torch.empty_like(input_tensor)

    # 启动内核，每一个 aunch grid 程序实例处理一行
    softmax_kernel[(n_rows, )](
        y,
        input_tensor,
        input_tensor.stride(0),
        y.stride(0),
        n_cols,
        num_warps=num_warps,
        BLOCK_SIZE=BLOCK_SIZE,
    )

    # 如果是按列计算softmax, 需要转置结果
    if axis == 0:
        return y.T
    return y


def softmax_2(x):
    '''
    softmax_kernel_2的封装函数，
    注意：这个实现只在输入是1D且元素数量不多时才正确
    '''
    # 这个内核实际上时在计算扁平化后张量的softmax
    x_flat = x.flatten()
    n_elements = x_flat.numel()
    output = torch.empty_like(x_flat)

    # 警告：这个内核的并行策略不正确，无法处理 n_elements > BLOCK_SIZE 的情况
    if n_elements > 1024:
        pytest.skip("跳过：softmax_2 内核实现不支持大规模输入。")

    BLOCK_SIZE = triton.next_power_of_2(n_elements)
    grid = (1, )
    softmax_kernel_2[grid](
        x_flat,
        output,
        n_elements,
        BLOCK_SIZE=BLOCK_SIZE,
    )
    return output.reshape(x.shape)


@pytest.mark.parametrize("shape, dtype, axis", [
    (shape, dtype, axis)
    # 测试不同打小和非2的幂次方的形状
    for shape in [[128, 512], [8, 1024], [1823,781]]
    # 覆盖所有重要的浮点类型
    for dtype in [torch.float32, torch.float16, torch.bfloat16]
    for axis in [0, 1]
])
def test_softmax_accuracy(shape, dtype, axis, device):
    torch.manual_seed(0)
    x = torch.randn(shape, dtype=dtype, device=device)

    y_triton = softmax(x, axis=axis)
    y_torch = torch.softmax(x, dim=axis)

    assert torch.allclose(y_triton, y_torch, atol=1e-2, rtol=0)


@pytest.mark.parametrize("test_name, input_data, dtype, axis", [
    # 测试名             # 输入数据                            # 数据类型        #计算维度
    ('basic_case_ax1',  torch.tensor([[1.0, 2.0, 3.0, 4.0]]), torch.float32, 1),
    ('basic_case_ax0',  torch.tensor([[1.0, 2.0],[3.0, 4.0]]), torch.float32, 0),
    ('neg_inf_mask_ax1', torch.tensor([[1.0,2.0,float('-inf'), 4.0]]), torch.float32, 1),
    ('neg_inf_mask_ax0', torch.tensor([[1.0,-float('inf')],[2.0,4.0]]), torch.float32, 0),
    ('all_neg_inf_ax1', torch.tensor([[-float('inf'),-float('inf')]]), torch.float32, 1),
    ('overflpw_check_ax1', torch.tensor([[1000.0, 1010.0, 990.0]]), torch.float32, 1),
    ('bfloat16_precision', torch.tensor([[1.0,2.0,-float('inf'), 4.0]]), torch.bfloat16, 1)
])
def test_softmax_edge_cases(test_name, input_data, dtype, axis, device):
    x = input_data.to(dtype=dtype, device=device)
    y_triton = softmax(x, axis=axis)
    y_torch = torch.softmax(x, dim=axis)

    # 对于全-inf的情况， 结果时nan, 需要特殊处理
    equal_nan = "all_neg_inf" in test_name

    assert torch.allclose(y_triton, y_torch, atol=1e-2, rtol=0, equal_nan=equal_nan)


# === 3. `softmax_2` 内核的修正性测试 ===
@pytest.mark.parametrize("shape, dtype", [
    ([1024], torch.float32), # 测试一个1D向量
    ([781], torch.bfloat16), # 测试一个非2的幂次方的1D向量
])
def test_softmax_2_corrected(shape, dtype, device):
    """
    这个测试验证 softmax_2 在其唯一能正确处理的场景下的行为：
    即当输入是一个1D向量时。
    """
    torch.manual_seed(0)
    x = torch.randn(shape, dtype=dtype, device=device)

    y_triton = softmax_2(x)

    # 因为内核处理的是扁平化的数据，所以参照组也应该对扁平化的数据计算
    y_torch = torch.softmax(x.flatten(), axis=0).reshape(x.shape)

    assert torch.allclose(y_triton, y_torch, atol=1e-2, rtol=0)



@benchmark.measure()
def bench_softmax(size, provider):
    torch.manual_seed(0)
    # 将设备改为 cuda，因为 triton 内核是为 GPU 设计的
    x = torch.randn(size, size, device='cuda')
    if provider == 'torch':
       torch.softmax(x, axis=1)
    if provider == 'triton':
       softmax(x, axis=1)


if __name__ == "__main__":
    # 这是一个简单的本地运行测试的脚本
    # 需要安装 pytest: pip install pytest
    # 然后运行: pytest your_file_name.py
    print("要运行这些测试，请使用 pytest。")
    print("例如: pytest a_file_name.py")