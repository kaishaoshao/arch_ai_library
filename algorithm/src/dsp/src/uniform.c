#include "dsp.h"

/// @brief 产生（a,b）区间上均匀分布随机数
/// @param a 给定区间的下限
/// @param b 给定区间的上限
/// @param seed 随机数种子
/// @return t 均匀分布的随机数
double uniform(double a, double b, long int *seed) {
    double t;
    *seed = 2045 * (*seed) + 1; // 更新种子：混合同余法迭代
    // x % m = x - (x / m) * m 
    *seed = (*seed) - (*seed / 1048576) * 1048576; // 取模操作：等效于 *seed % 1048576
    t = (*seed) / 1048576.0;  // 0.0 <= t <= 1.0
    t = a + t * (b - a);      // a   <= t <= b 
    return t;
}

#ifdef TEST

// 产生50个 0 到 1 之间均匀分布的随机数

#include <stdio.h>

int main() {
    double x;
    double a = 0.0;
    double b = 1.0;
    long int seed = 13579;
    
    for(int i = 0; i < 5; i++) {
        for(int j = 0; j < 10; j++) {
            x = uniform(a, b, &seed);
            printf("%.7f", x);
        }
       printf("\n");
    }
    return 0;
}

#endif
