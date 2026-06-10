#include <stdio.h>
#include <stdlib.h>
#include <math.h> 

#include <cuda_runtime.h>

// 任务1: 修改内核
// FMA: C[i] = A[i] * B[i] + C[i]
__global__ void GPUfma(const float *A, const float *B, float *C, const int n)
{
  int i = blockDim.x * blockIdx.x + threadIdx.x;

  if(i < n) {
      C[i] = A[i] * B[i] + C[i];
    }
} 

// 任务6: CPU实现FMA
void CPUfma(const float *A, const float *B, float *C, const int n) 
{
	for (int i = 0; i < n; i++)
	{
		// C[i] = A[i] * B[i] + C[i]
		C[i] = fmaf(A[i], B[i], C[i]); 
	}
}

// 任务2: 检查错误的宏
#define CUDA_CHECK(call)                           \
do {                                               \
	cudaError_t err = call;                          \
	if(err != cudaSuccess) {                         \
		fprintf(stderr, "CUDA error at %s: %d: %s\n",  \
			      __FILE__, __LINE__,                    \
	        cudaGetErrorString(err));                \
	exit(EXIT_FAILURE);                              \				
	}                                                \
} while (0)

/// @brief 运行测试
/// @param n   
/// @param mode 1 UM模式  0 EM模式 
void run_test(int n, int mode) {
	size_t size = n * sizeof(float);
	float *h_A, *h_B, *h_C, *h_C_ref;
	float *d_A, *d_B, *d_C;
  float t_h2d = 0, t_ker = 0, t_d2h = 0;

	// 创建事件
	cudaEvent_t start, stop;
	CUDA_CHECK(cudaEventCreate(&start));
	CUDA_CHECK(cudaEventCreate(&stop)); 

	// 显存内存模式
	if(mode == 0) 
	{ 
		 h_A = (float *) malloc(size);
		 h_B = (float *) malloc(size);
		 h_C = (float *) malloc(size);

		 for (int i = 0; i < n; i++)
		 {
		   h_A[i] = 1.0f;
			 h_B[i] = 2.0f;
			 h_C[i] = 3.0f; 
		 }
		 CUDA_CHECK(cudaMalloc(&d_A, size));
		 CUDA_CHECK(cudaMalloc(&d_B, size));
		 CUDA_CHECK(cudaMalloc(&d_C, size));
		 
		 // 任务3 : 测量H2D
		 CUDA_CHECK(cudaEventRecord(start));
		 CUDA_CHECK(cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice));
		 CUDA_CHECK(cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice));
		 CUDA_CHECK(cudaMemcpy(d_C, h_B, size, cudaMemcpyHostToDevice));
		 CUDA_CHECK(cudaEventRecord(stop));
		 CUDA_CHECK(cudaEventSynchronize(stop));
		 CUDA_CHECK(cudaEventElapsedTime(&t_d2h, start, stop));

	}
	else  // 任务9: 统一内存模式 
	{
		CUDA_CHECK(cudaMallocManaged(&d_A, size));
		CUDA_CHECK(cudaMallocManaged(&d_B, size));
		CUDA_CHECK(cudaMallocManaged(&d_C, size));
		for (int i = 0; i < n; i++)
		{
			d_A[i] = 1.0f;
			d_B[i] = 2.0f;
			d_C[i] = 3.0f;
		}		
	}

	// 任务4: 测量内核时间
	int threadsPerBlock = 256;
	int blocksPerGrid = (n + threadsPerBlock -1) / threadsPerBlock;
	CUDA_CHECK(cudaEventRecord(start));
	GPUfma<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, n);
	CUDA_CHECK(cudaEventRecord(stop));
	CUDA_CHECK(cudaEventSynchronize(stop));
	cudaEventElapsedTime(&t_ker, start, stop);

	if(mode == 0) { // 显式内存模式 D2H
		// 任务5: 测量D2H
		CUDA_CHECK(cudaEventRecord(start));
		CUDA_CHECK(cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost));
		CUDA_CHECK(cudaEventSynchronize(stop));
		CUDA_CHECK(cudaEventElapsedTime(&t_d2h, start, stop));
		
		free(h_A);
		free(h_B);
		free(h_C);

		CUDA_CHECK(cudaFree(d_A));
		CUDA_CHECK(cudaFree(d_B));
		CUDA_CHECK(cudaFree(d_C));
	}
	else
	{ // UM模式数据就在d_C中,只需要同步即可访问
		CUDA_CHECK(cudaDeviceSynchronize());

		CUDA_CHECK(cudaFree(d_A));
		CUDA_CHECK(cudaFree(d_B));
		CUDA_CHECK(cudaFree(d_C));
	}

	printf("%-10s | %10d | %8.3f | %8.3f | %8.3f | %8.3f\n", mode == 0 ? "EM" : "UM", n, t_h2d, t_ker, t_d2h, t_h2d + t_ker + t_d2h);
}

int main() {
	int sizes[] = {1000, 10000, 100000, 1000000, 10000000};
	printf("%-10s | %10s | %8s | %8s | %8s | %8s\n", "Mode", "Size", "H2D(ms)", "Ker(ms)", "D2H(ms)", "Total(ms)");
	printf("----------------------------------------------------------------------\n");

	for (int i = 0; i < 5; i++)
	{
		run_test(sizes[i], 0); // EM 模式
		run_test(sizes[i], 1); // UM 模式
	}
	
	return 0;

}
