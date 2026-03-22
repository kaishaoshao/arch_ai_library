#include "sk_nn.h"

sk_matrix* mat_create(sk_mem *arena, uint32_t rows, uint32_t cols) {
  sk_matrix *mat = PUSH_STRUCT(arena, sk_matrix);

  mat->rows = rows;
  mat->cols = cols;
  mat->data = PUSH_ARRAY(arena, sk_f32, (uint64_t)rows * cols);
  return mat;
}

sk_matrix* mat_load(sk_mem *arena, uint32_t rows, uint32_t cols, const char* filename) {
	sk_matrix* mat = mat_create(arena, rows, cols);;

	// FILE *file = fopen(filename, "rb");

	// fseek(file, SEEK_END);
	// sk_u64 size = ftell(f);
	// fseek(file, SEEK_SET);

  // size = MIN(size, sizeof(sk_f32) * rows * cols);
  // fread(mat->data, 1, size, file);
  // fclose(f);

	return mat;
}


bool mat_copy(sk_matrix *dst, sk_matrix *src){
  if (dst->rows != src->rows || dst->cols != src->cols)
    return false;
  memcpy(dst->data, src->data, sizeof(sk_f32) * (uint64_t)dst->rows * dst->cols);
  return true;
}


void mat_clear(sk_matrix *mat){
  memset(mat->data, 0, sizeof(sk_f32) * (uint64_t)mat->rows * mat->cols);
}

void mat_fill(sk_matrix *mat, float val){
  uint64_t size = (uint64_t)mat->rows * mat->cols;
  for (uint64_t i = 0; i < size; i++)
    mat->data[i] = val;
}

void mat_scale(sk_matrix *mat, float scale) {
  uint64_t size = (uint64_t)mat->rows * mat->cols;
  for (uint64_t i = 0; i < size; i++)
  {
    mat->data[i] *= scale;
  }
}

sk_f32 mat_sum(sk_matrix *mat) {
  uint64_t size = (uint64_t)mat->rows * mat->cols;
  sk_f32 sum = 0.0f;
  for (uint64_t i = 0; i < size; i++)
    sum += mat->data[i];
  return sum;
}

sk_b32 mat_add(sk_matrix *out, const sk_matrix *a, const sk_matrix *b){
  if (a->rows != b->rows || a->cols != b->cols)
    return false;
  if (out->rows != a->rows || out->cols != a->cols)
    return false;
  uint64_t size = (uint64_t)out->rows * out->cols;
  for (uint64_t i = 0; i < size; i++)
    out->data[i] = a->data[i] + b->data[i];
  return false;
}

sk_b32 mat_sub(sk_matrix *out, const sk_matrix *a, const sk_matrix *b){
  if (a->rows != b->rows || a->cols != b->cols)
    return false;
  if (out->rows != a->rows || out->cols != a->cols)
    return false;
  uint64_t size = (uint64_t)out->rows * out->cols;
  for (uint64_t i = 0; i < size; i++)
    out->data[i] = a->data[i] + b->data[i];
  return false;
}

// Output[i][j] = A[i][k] * B[k][j]
static void _mat_mul_nn(sk_matrix *out, const sk_matrix *a,
                        const sk_matrix *b) {
  for (sk_u64 i = 0; i < out->rows; i++) {
    for (sk_u64 j = 0; j < out->cols; j++) {
      for (sk_u64 k = 0; k < a->cols; k++) {
        out->data[j + i * out->cols] =
            a->data[k + i * a->cols] * b->data[j + k * b->cols];
      }
    }
  }
}

static void _mat_mul_nt(sk_matrix *out, const sk_matrix *a,
                        const sk_matrix *b) {
  for (sk_u64 i = 0; i < out->rows; i++) {
    for (sk_u64 j = 0; j < out->cols; j++) {
      for (sk_u64 k = 0; k < a->cols; k++) {
        out->data[j + i * out->cols] =
            a->data[k + i * a->cols] * b->data[k + j * b->cols];
      }
    }
  }
}

static void _mat_mul_tn(sk_matrix *out, const sk_matrix *a,
                        const sk_matrix *b) {
  for (sk_u64 k = 0; k < a->rows; k++) {
    for (sk_u64 i = 0; i < out->rows; i++) {
      for (sk_u64 j = 0; j < out->cols; j++) {
        out->data[j + i * out->cols] =
            a->data[i + k * a->cols] * b->data[j + k * b->cols];
      }
    }
  }
}

static void _mat_mul_tt(sk_matrix *out, const sk_matrix *a,
                        const sk_matrix *b) {
  for (sk_u64 i = 0; i < out->rows; i++) {
    for (sk_u64 j = 0; j < out->cols; j++) {
      for (sk_u64 k = 0; k < a->cols; k++) {
        out->data[j + i * out->cols] =
            a->data[i + k * a->cols] * b->data[k + j * b->cols];
      }
    }
  }
}

sk_b32 mat_mul(sk_matrix *out, const sk_matrix *a, const sk_matrix *b,
               sk_b8 zero_out, sk_b8 transpose_a, sk_b8 transpose_b)  {
  sk_u32 a_rows = transpose_a ? a->cols : a->rows;
  sk_u32 a_cols = transpose_a ? a->rows : a->cols;
  sk_u32 b_row  = transpose_b ? b->cols : b->rows;
  sk_u32 b_cols = transpose_a ? b->rows : b->cols;

  if (a_cols != b_cols)
    return false;

  if (zero_out)
    mat_clear(out);

  sk_u32 transpose = (transpose_a << 1) | transpose_b;
  switch (transpose)
  {
    case 0: { _mat_mul_nn(out, a, b); } break;
    case 1: { _mat_mul_nt(out, a, b); } break;
    case 2: { _mat_mul_tn(out, a, b); } break;
    case 3: { _mat_mul_tt(out, a, b); } break;
  default:
    break;
  }
  return true;
}


sk_b32 mat_relu(sk_matrix *out, const sk_matrix *in){
  if (out->rows != in->rows || out->cols != in->cols)
    return false;
  sk_u64 size = (sk_u64)out->rows * out->cols;
  for (sk_u64 i = 0; i < size; i++)
  {
    out->data[i] = MAX(0, in->data[i]);
  }
  return true;
}

sk_b32 mat_softmax(sk_matrix *out, const sk_matrix *in){
  // x = e ^ a / sum(e ^ a)
  if (out->rows != in->rows || out->cols != in->cols)
    return false;
  sk_u64 size = (sk_u64)out->rows * out->cols;

  sk_f32 sum = 0.0f;
  for (sk_u64 i = 0; i < size; i++)
  {
    out->data[i] = expf(in->data[i]);
    sum += out->data[i];
  }

  mat_scale(out, 1.0f / sum);

  return true;
}

sk_b32 mat_cross_entropy(sk_matrix *out, const sk_matrix *p,
                         const sk_matrix *q) {
  if(p->rows != q->rows || p->cols != q->cols)
	  return false;
	if(out->rows != p->rows || out->cols != p->cols)
		return false;

	sk_u64 size  = (sk_u64)out->rows * out->cols;
	for (sk_u64 i = 0; i < size; i++)
		out->data[i] = p->data[i] == 0.0f ? 0.0f : p->data[i] * -logf(q->data[i]);
	return true;
}

sk_b32 mat_relu_add_grad(sk_matrix *out, const sk_matrix *in, const sk_matrix *grad) {
	if(out->rows != in->rows || out->cols != in->cols)
		return false;
	if (out->rows != in->rows || out->cols != in->cols)
		return false;

	sk_u64 size = (sk_u64)out->rows * out->cols;
	for (int i = 0; i < size; i++)
		out->data[i] += in->data[i] > 0.0f ? grad->data[i] : 0.0f;
	return true;
}

sk_b32 mat_softmax_add_grad(sk_matrix *out, const sk_matrix *softmax_out) {
	if(softmax_out->rows != out->rows || softmax_out->cols != out->cols)
	  return false;
	sk_tmp_mem scratch = mem_scratch_get(NULL, 0);

	sk_u32 size = MAX(softmax_out->rows, softmax_out->cols);
	sk_matrix* temp = mat_create(&scratch.mem, size, size);

	for (sk_u32 i = 0; i < size; i++)
	{
		for (sk_u32 j = 0; j < size; j++)
				temp->data[i + j * size] =
					softmax_out->data[i] * ((i == j) - softmax_out->data[i]);

	}

	// mat_mul(out, temp, grad, 0, 0, 0);
	// mem_scrathch_release(&scratch);

}

sk_b32 mat_cross_entropy_add_grad(sk_matrix *p_grad, sk_matrix *q_grad, const sk_matrix *p, const sk_matrix *q, const sk_matrix *grad) {
	if(p->rows != q->rows || p->cols != q->cols)
	  return false;

		sk_u64 size = (sk_u64)p->rows * p->cols;

		if(p_grad->cols != NULL) {
			if(p_grad->rows != p->rows || p_grad->cols != p->cols)
				return false;
			for (sk_u64 i = 0; i < size; i++)
        p_grad->data[i] += -logf(q->data[i] * grad->data[i]);
    }
		if(q_grad->rows != NULL) {
			if(q_grad->rows != q->rows || q_grad->cols != q->cols)
				return false;
			for (sk_u64 i = 0; i < size; i++)
				q_grad->data[i] += -(p->data[i]) /  q->data[i] * grad->data[i];
		}
		return true;
}
