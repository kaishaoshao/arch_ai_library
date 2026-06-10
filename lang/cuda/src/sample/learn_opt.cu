#include <stdio.h>
#include <cuda_runtime.h>
#include <chrono>

// 循环次数：10亿次。
// 对于未优化的 CPU/GPU 来说足够长，能感觉到延迟。
#define ITERATIONS 1000000000L

// ==========================================
// GPU 内核：一个会被优化掉的“忙等待”循环
// ==========================================
__global__ void uselessLoopKernel(long long* out) {
    long long sum = 0;
    // 这是一个极其低效的循环。
    // 如果开启了优化器，它会发现 'sum' 的最终结果是可以预计算的，
    // 或者发现这个循环对外界没有任何影响，从而直接删除整个循环。
    for (long long i = 0; i < ITERATIONS; ++i) {
        sum += 1;
    }
    // 我们写入结果，防止编译器认为 sum 变量完全没用。
    // 但智能的优化器仍然能把上面的循环简化成 *out = ITERATIONS;
    *out = sum;
}

// ==========================================
// CPU 函数：同样的“忙等待”循环
// ==========================================
void cpuUselessLoop() {
    printf("  CPU 正在执行 %ld 次循环 (请耐心等待)...\n", ITERATIONS);
    auto start = std::chrono::high_resolution_clock::now();

    long long sum = 0;
    // 如果主机编译器使用默认的 -O0，它会老实执行这个循环。
    // 如果使用了 -O2 或 -O3，这个循环会被瞬间跳过。
    for (long long i = 0; i < ITERATIONS; ++i) {
        sum += i % 2; // 做点稍微复杂的操作防止极度简单的常量折叠
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff = end - start;
    // 使用 sum 防止它被完全优化掉，虽然没打印它。
    if (sum > 0) {
         printf("  CPU 耗时: %.4f 秒\n", diff.count());
    }
}


int main() {
    printf("=== 开始测试 nvcc 默认优化行为 ===\n\n");

    // --- 测试 1: CPU 性能 ---
    printf("[测试 1] 主机端 (CPU) 代码执行:\n");
    cpuUselessLoop();
    printf("\n");

    // --- 测试 2: GPU 性能 ---
    printf("[测试 2] 设备端 (GPU) 代码执行:\n");
    long long* d_out;
    long long h_out = 0;
    cudaMalloc(&d_out, sizeof(long long));

    // 使用 CUDA 事件进行精确计时
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    printf("  GPU 内核启动...\n");
    cudaEventRecord(start);
    // 启动内核，1个线程块，1个线程
    uselessLoopKernel<<<1, 1>>>(d_out);
    cudaEventRecord(stop);

    // 等待 GPU 完成
    cudaDeviceSynchronize();

    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    printf("  GPU 耗时: %.4f 毫秒 (即 %.4f 秒)\n", milliseconds, milliseconds / 1000.0);

    cudaMemcpy(&h_out, d_out, sizeof(long long), cudaMemcpyDeviceToHost);
    // printf("Debug output: %lld\n", h_out);

    // 清理
    cudaFree(d_out);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    printf("\n=== 测试结束 ===\n");
    printf("结果分析提示：\n");
    printf("如果耗时在 0.00xx 秒级别，说明循环被优化掉了（快）。\n");
    printf("如果耗时在 秒 级别，说明循环老实执行了（慢）。\n");

    return 0;
}
