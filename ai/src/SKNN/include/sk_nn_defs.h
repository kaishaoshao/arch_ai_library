#ifndef __SK_NN_CONFIG_H__
#define __SK_NN_CONFIG_H__

#include <float.h>
#include <stdint.h>
#include <stdbool.h>
#include <inttypes.h>

typedef _Float16 sk_f16;
typedef float    sk_f32;
typedef double   sk_f64;

typedef _Bool    sk_bool;

typedef int8_t   sk_b8;
typedef int16_t  sk_b16;
typedef int32_t  sk_b32;
typedef int64_t  sk_b64;

typedef uint8_t  sk_u8;
typedef uint16_t sk_u16;
typedef uint32_t sk_u32;
typedef uint64_t sk_u64;

// 内存大小
#define KiB(n) ((sk_u64)(n) << 10)
#define MiB(n) ((sk_u64)(n) << 20)
#define GiB(n) ((sk_u64)(n) << 30)

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) < (b)) ? (a) : (b))

// 整数 n 向上对齐到 p 的整数倍
#define ALIGN_UP_POW2(n, p)                           \
  (((sk_u64)(n) + ((sk_u64)(p) - 1)) & (sk_u64)(p) - 1)

#endif // __SK_NN_CONFIG_H__
