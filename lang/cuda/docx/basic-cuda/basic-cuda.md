https://github.com/eunomia-bpf/basic-cuda-tutorial

## CUDA编程模型

每一个CUDA程序都遵循类似的模式：

1. 在CPU(主机) 和 GPU(设备)上分配内存
2. 将输入数据从CPU复制到GPU
3. 启动在GPU上运行的内核(函数)
4. 将结果从GPU上运行的内核(函数)
5. 清理所有分配的内存
   与常规C编程相比，这个工作流程可能看起来很冗长，但是这个必要的，因为CPU和GPU有独立的内存空间。数据必须在它们之间显式移动。

### 线程索引

每个GPU线程都需要知道它应该处理数组的哪个元素。公式 `blockDim.x * blockIdx.x + threadIdx.x`为每个线程计算一个唯一的全局索引。

为了可视化这一点，假设我们有50,000个元素，我们将GPU线程组织成每个块256个线程。我们需要196个块（从50000/256向上取整）。索引的工作方式如下：

* 块0中的线程0：索引 = 256 * 0 + 0 = 0
* 块0中的线程5：索引 = 256 * 0 + 5 = 5
* 块1中的线程0：索引 = 256 * 1 + 0 = 256
* 块2中的线程100：索引 = 256 * 2 + 100 = 612

边界检查 `if (i < numElements)`至关重要，因为我们的最后一个块可能有超出数组大小的线程(前面是向上取整)。没有这个检查，这些线程会访问无效内存。

### CUDA中内存管理

```cpp
// 主机（CPU）内存
float *h_A = (float *)malloc(size);

// 设备（GPU）内存
float *d_A = NULL;
cudaMalloc((void **)&d_A, size);
```

使用命名约定，其中 `h_`前缀表示主机内存，`d_`前缀表示设备内存。这有助于防止常见错误，比如将GPU指针传递给CPU函数。

### 主机和设备之间数据传输

在两侧分配内存后，我们需要将输入数据复制到GPU中：

```cpp
cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);
```

`cudaMemcpy`函数是同步的，意味着CPU会等待传输完成后再继续。第四个参数指定方向：`cudaMemcpyHostToDevice`表示CPU到GPU，`cudaMemcpyDeviceToHost`表示GPU到CPU。

这些内存传输可能成为性能瓶颈。**经验法则是，你希望最小化传输次数，并最大化在传输之间在GPU上执行的计算量。**

### 启动内核

```cpp
int threadsPerBlock = 256;
int blocksPerGrid = (numElements + threadsPerBlock - 1) / threadsPerBlock;
vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, numElements);
```

三角括号语法 `<<<blocksPerGrid, threadsPerBlock>>>`是CUDA指定执行配置的方式。我们告诉GPU启动196个块，每个块256个线程，总共给我们50,176个线程（略多于我们的50,000个元素）。向上取整除法公式 `(numElements + threadsPerBlock - 1) / threadsPerBlock`确保我们总是有足够的线程来覆盖所有元素

### 错误检查

CUDA内核启动是异步的，意味着CPU不会等待内核完成。内核中的错误不会立即显示。这就是为什么我们检查启动错误：

```cpp
cudaError_t err = cudaGetLastError();
if (err != cudaSuccess) {
    fprintf(stderr, "Failed to launch kernel: %s\n", cudaGetErrorString(err));
    exit(EXIT_FAILURE);
}
```

这捕获配置错误，如请求每个块太多线程或GPU内存不足。在开发期间，始终在内核启动和CUDA API调用后检查错误。

### 验证和清理

将结果复制回主机后，我们验证计算:

```cpp
for (int i = 0; i < numElements; ++i) {
    if (fabs(h_A[i] + h_B[i] - h_C[i]) > 1e-5) {
        fprintf(stderr, "Result verification failed at element %d!\n", i);
        exit(EXIT_FAILURE);
    }
}
```

小epsilon（1e-5）的浮点比较

释放所有分配的内存

```cpp
cudaFree(d_A);  // 释放GPU内存
free(h_A);      // 释放CPU内存
```

忘记释放内存会导致泄漏。GPU内存通常比系统RAM更有限，所以泄漏会很快引起问题。

测量性能

```cpp
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);

cudaEventRecord(start);
```

启动内核后

```cpp
cudaEventRecord(stop);
cudaEventSynchronize(stop);

float milliseconds = 0;
cudaEventElapsedTime(&milliseconds, start, stop);
printf("Kernel execution time: %.3f ms\n", milliseconds);

cudaEventDestroy(start);
cudaEventDestroy(stop);
```

### 内存带宽分析

向量加法是内存受限操作，意味着性能受限于我们读写数据的速度，而不是计算速度。让我们计算实现的内存带宽：

对于50,000个元素： - 我们读取两个float数组：50,000 * 4字节 * 2 = 400 KB - 我们写入一个float数组：50,000 * 4字节 = 200 KB - 总内存流量：600 KB

如果你的内核在0.1毫秒内运行，带宽是： - 600 KB / 0.0001秒 = 6 GB/s

将此与你的GPU的理论带宽进行比较（检查 `nvidia-smi`或GPU规格）。例如，RTX 5090的理论带宽约为1792 GB/s。如果你实现了100-200 GB/s，对于一个简单的内核来说已经做得很好了。

理论带宽和实现带宽之间的差距来自几个因素：内存访问模式、缓存行为和PCIe传输开销。我们将在后面的教程中探索优化。

内存合并访问

相邻的线程（在warp内）访问相邻的内存位置。这允许GPU将多个内存请求合并为单个宽事务。

修改内核以跨步模式访问内存：

```cpp
int i = (blockDim.x * blockIdx.x + threadIdx.x) * 2;  // 跳过每个其他元素
if (i < numElements) {
    C[i] = A[i] + B[i];
}
```

你需要启动两倍的线程并调整边界检查。对这个版本计时并比较。非合并访问模式会明显更慢，因为每个内存请求都需要单独的事务。

### 调试

当出现问题时，CUDA提供了几个调试工具：

**cuda-memcheck：** 检测内存错误，如越界访问

```
cuda-memcheck./01-vector-addition
```

**cuda-gdb：** GPU调试器，用于逐步调试

```
cuda-gdb./01-vector-addition
```

**Compute Sanitizer：** cuda-memcheck的现代替代品

```
compute-sanitizer./01-vector-addition
```

要注意的常见错误： - 将主机指针传递给内核（会导致段错误） - 忘记从设备复制数据回来 - 不检查CUDA错误代码 - 访问超出数组边界的内存 - 内存分配和释放调用不匹配

### 分析代码

**Nsight Systems** 用于时间线分析：

```
nsysprofile--stats=true./01-vector-addition
```

这准确显示时间花在哪里：内存传输、内核执行和CPU代码。

**Nsight Compute** 用于内核分析：

```
ncu--setfull./01-vector-addition
```

这提供了关于内存带宽、SM利用率和性能瓶颈的详细指标。

### 常见问题和解决方案

**错误："CUDA driver version is insufficient"** 你的驱动程序对于你的CUDA工具包版本来说太旧了。更新你的NVIDIA驱动程序。

**错误："out of memory"** GPU没有足够的内存。减少 `numElements`或分批处理数据。

**错误："invalid device function"** 内核是为不同的GPU架构编译的。检查你的Makefile中的 `-arch`标志是否与你的GPU的计算能力匹配。

**段错误：** 可能是将主机指针传递给内核或访问未分配的内存。使用 `cuda-memcheck`诊断。

**结果不正确：** 检查你的索引计算。添加边界检查并首先用较小的数据集验证。

## 使用PTX理解GPU汇编

### 什么是PTX

它不会直接变成在GPU上运行的机器指令,PTX处于高级CUDA C++和低级GPU机器代码（SASS）之间的最佳位置。

可以把PTX看作是一种中间语言，类似于Java字节码或LLVM IR。优势如下.

 架构独立性:

性能调优性,理解编译器输出,低级控制
