#ifndef __MATH_RVV_ONNX_RVV_H
#define __MATH_RVV_ONNX_RVV_H

#include "onnx.h"

void abs_rvv_int8(struct onnx_node_t *n);
void abs_rvv_int16(struct onnx_node_t *n);
void abs_rvv_int32(struct onnx_node_t *n);


void abs_rvv_f8(struct onnx_node_t *n);
void abs_rvv_f16(struct onnx_node_t *n);
void abs_rvv_f32(struct onnx_node_t *n);

#endif // __MATH_RVV_ONNX_RVV_H
