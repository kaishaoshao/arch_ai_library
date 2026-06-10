#include <stdio.h>


__global__ void hello_from_gpu()
{
    printf("Hello World from the GPU!\n");
}



int main(void)
{
    // 核函数调用  1.线程块数量 2.线程块里面线程数量
    hello_from_gpu<<<3,1>>>();
    // 主机代码
    cudaDeviceSynchronize();
    return 0;
}
