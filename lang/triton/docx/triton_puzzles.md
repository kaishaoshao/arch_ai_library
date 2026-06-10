# triton算子学习

## 原语

### tl.program_id(0)

#### 含义

获取当前线程块在第一维度0轴上的全局索引

* 如果启动内核时指定grid=(4,), 则pid取值0，1，2，3

为什么是program_id而不是thread_id:

Triton 的编程模型是块级并行（类似CUDA的block)，而非线程级。每个program_id对应的一个独立的并行任务单元。

### pid * B0 + tl.arange(0，B0)的数学意义

实现了数据块的全局内存偏移计算：

pid * B0：当前线程处理的起始地址在全局内存中的偏移

例如 pid = 1， B0=128 ——> 偏移128

**`tl.arange(0, B0)`**：生成一个从 `0`到 `B0-1`的连续序列，表示块内元素的 **相对偏移**



参考文章

https://zhuanlan.zhihu.com/p/20539246076
