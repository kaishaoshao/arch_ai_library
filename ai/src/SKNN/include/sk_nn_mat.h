#ifndef __SK_NN_MAT_H__
#define __SK_NN_MAT_H__

#include "sk_nn.h"

typedef struct
{
    uint32_t  rows;
    uint32_t  cols;
    sk_f32   *data;
}sk_matrix;

/// @brief
/// @param arena
/// @param rows
/// @param clos
/// @return
sk_matrix* mat_create(sk_mem *arena, uint32_t rows, uint32_t clos);

/// @brief
/// @param arena
/// @param rows
/// @param clos
/// @param filename
/// @return
sk_matrix* mat_load(sk_mem *arena, uint32_t rows, uint32_t clos, const char* filename);

/// @brief
/// @param dst
/// @param src
sk_bool mat_copy(sk_matrix *dst, sk_matrix *src);

/// @brief
/// @param mat
void mat_clear(sk_matrix *mat);

/// @brief
/// @param mat
/// @param val
void mat_fill(sk_matrix *mat, float val);

/// @brief
/// @param mat
/// @param val
void mat_scale(sk_matrix *mat, float val);

/// @brief
/// @param out
/// @param a
/// @param b
/// @return
sk_b32 mat_add(sk_matrix *out, const sk_matrix *a, const sk_matrix *b);

/// @brief
/// @param out
/// @param a
/// @param b
/// @return
sk_b32 mat_sub(sk_matrix *out, const sk_matrix *a, const sk_matrix *b);

/// @brief
/// @param out
/// @param a
/// @param zer_out
/// @param transpose_a
/// @param transpose_b
/// @return
sk_b32 mat_mul(sk_matrix *out, const sk_matrix *a, const sk_matrix *b,
               sk_b8 zer_out, sk_b8 transpose_a, sk_b8 transpose_b);

/// @brief
/// @param out
/// @param in
/// @return
sk_b32 mat_relu(sk_matrix *out, const sk_matrix *in);

/// @brief
/// @param out
/// @param in
/// @return
sk_b32 mat_softmax(sk_matrix *out, const sk_matrix *in);

/// @brief
/// @param out
/// @param p
/// @param q
/// @return
sk_b32 mat_cross_entropy(sk_matrix *out, const sk_matrix *p, const sk_matrix *q);

/// @brief
/// @param out
/// @param in
/// @return
sk_b32 mat_relu_add_grad(sk_matrix *out, const sk_matrix *in, const sk_matrix *grad);

/// @brief
/// @param out
/// @param softmax_out
/// @return
sk_b32 mat_softmax_add_grad(sk_matrix *out, const sk_matrix *softmax_out);

/// @brief
/// @param out
/// @param p
/// @param q
/// @param grad
/// @return
sk_b32 mat_cross_entropy_add_grad(sk_matrix *p_grad, sk_matrix *q_grad,
                const sk_matrix *p, const sk_matrix *q, const sk_matrix *grad);

#endif // __SK_NN_MAT_H__
