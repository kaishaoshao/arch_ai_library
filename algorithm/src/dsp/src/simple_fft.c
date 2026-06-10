#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <stdlib.h> // 需要 malloc 和 free

#define PI 3.14159265358979323846

// 定义复数结构体
typedef struct {
    float real;
    float imag;
} Complex;

// ---------------------------------------------------------
// 第一部分：位反转 (Bit Reversal)
// ---------------------------------------------------------
void bit_reversal(Complex* data, int N) {
    int j = 0;
    for (int i = 0; i < N - 1; i++) {
        if (i < j) {
            Complex temp = data[i];
            data[i] = data[j];
            data[j] = temp;
        }
        int k = N / 2;
        while (k <= j) {
            j -= k;
            k /= 2;
        }
        j += k;
    }
}

// ---------------------------------------------------------
// 第二部分：简单的 Radix-2 FFT 实现
// ---------------------------------------------------------
void simple_fft(Complex* data, int N) {
    bit_reversal(data, N);

    int stages = (int)(log2(N));

    for (int s = 1; s <= stages; s++) {
        int m = 1 << s;
        int m2 = m / 2;

        Complex wm;
        wm.real = cos(PI / m2);
        wm.imag = -sin(PI / m2);

        for (int k = 0; k < N; k += m) {
            Complex w = {1.0, 0.0};
            for (int j = 0; j < m2; j++) {
                Complex u = data[k + j];
                Complex t_in = data[k + j + m2];

                Complex t;
                t.real = w.real * t_in.real - w.imag * t_in.imag;
                t.imag = w.real * t_in.imag + w.imag * t_in.real;

                data[k + j].real = u.real + t.real;
                data[k + j].imag = u.imag + t.imag;

                data[k + j + m2].real = u.real - t.real;
                data[k + j + m2].imag = u.imag - t.imag;

                Complex w_temp = w;
                w.real = w_temp.real * wm.real - w_temp.imag * wm.imag;
                w.imag = w_temp.real * wm.imag + w_temp.imag * wm.real;
            }
        }
    }
}

// ---------------------------------------------------------
// 主函数：修改为标准输入输出接口 (Standard I/O)
// ---------------------------------------------------------
int main() {
    int N;

    // 1. 从标准输入读取点数 N
    // Python 会先发送这个数字
    if (scanf("%d", &N) != 1) {
        return 1; // 读取错误
    }

    // 动态分配内存，因为 N 是变量
    Complex* test_data = (Complex*)malloc(sizeof(Complex) * N);
    if (test_data == NULL) return 1;

    // 2. 读取输入信号 (假设输入是实数信号)
    for (int i = 0; i < N; i++) {
        float val;
        if (scanf("%f", &val) == 1) {
            test_data[i].real = val;
            test_data[i].imag = 0.0f;
        } else {
            test_data[i].real = 0.0f;
            test_data[i].imag = 0.0f;
        }
    }

    // 3. 执行 C 语言实现的 FFT
    simple_fft(test_data, N);

    // 4. 输出结果到标准输出
    // 格式：实部 虚部 (每行一个复数)
    for (int i = 0; i < N; i++) {
        printf("%f %f\n", test_data[i].real, test_data[i].imag);
    }

    free(test_data);
    return 0;
}