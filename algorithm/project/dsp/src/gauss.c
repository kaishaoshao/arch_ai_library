#include "dsp.h"

/// @brief 产生正态分布N(u, sigma^2)的随机数
/// @param mean  正态分布的的均值u
/// @param sigma 正态分布的方差sigm
/// @param seed  随机数种子
/// @return y =  N(u, sigma^2)
double gauss(double mean, double sigma, long int *seed)
{ 
    double x, y;
    for (int i = 0; i < 12; i++)
       x += uniform(0.0, 1.0, seed);
    x -= 6.0;   
    y = sigma * x + mean;
    return y;
}

#ifdef TEST

// 产生50个均值为0，方差为1的正态分布随机数

#include <stdio.h>

int main()
{

}


#endif // TEST


