#include <stdio.h>

void printf_binary(unsigned int num) {
    if (num > 1)
        printf_binary(num >> 1);
    putchar((num & 1) ? '1' : '0');
}

int main()
{
    //操作最右边的位元
    {
    // x & （x - 1）
    // 作用：
    // 1. 消除二进制表示中最低位的1
    // 2. 判断一个数是不是2的幂
    // 0101 1110 -> 0101 1100
    int x1 = 0b01011110;
    printf_binary(x1);
    x1 = x1 & (x1 - 1);
		printf(" -> ");
		printf_binary(x1);
		puts("");
		// 8(1000) & 7(0111) = 0000 -> 是2的幂
		// 6(0110) & 5(0101) = 0100 != 0 不是2的幂
		x1 = 0b1000;
    for (int x = 6; x <= 8; x+=2)
      if ((x & (x - 1)) == 0)
        printf("x=%d 是2的幂\n", x);
      else
        printf("x=%d 不是2的幂\n", x);
		}

		{


		}

		return 0;
}
