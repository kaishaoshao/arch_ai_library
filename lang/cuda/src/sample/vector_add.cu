#include <assert.h>
#include <stdio.h>
#include <math.h>

// CUDA kernel for vector addition
__global__ void vectorAdd(int *a,int *b,int *c,int n)
{
    // Calculate global thread ID (tid)
    int tid = (blockIdx.x * blockDim.x) + threadIdx.x;
    // Vector boundary guard
    if(tid < n)
        // Each thread adds a single element
        c[tid] = a[tid] + b[tid];
}

// Initialize verctor of size n to int between 0-99
void matrix_init(int *a,int n)
{
    for(int i = 0; i < n; i++)
        a[i] = rand() % 100;
}

// Check vector add result
void error_check(int *a,int *b,int *c,int n)
{
    for (int i = 0; i < n; i++)
        assert(c[i] = a[i] + b[i]);
    
}

int main()
{
    // Array size of 2^16 (65536 elements)
    constexpr int N = 1 << 16;
    constexpr size_t bytes = sizeof(int) * N;

    

    return 0;
}