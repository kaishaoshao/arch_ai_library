#include "onnx.h"

void abs_int8(struct onnx_node_t *n)
{
    struct onnx_tensor_t *input = n->inputs[0];
    struct onnx_tensor_t *output = n->outputs[0];

    int8_t *px = (int8_t *)input->datas;
    int8_t *py = (int8_t *)output->datas;

    for (size_t i = 0; i < input->ndata; i++)
    {
        py[i] = px[i] < 0 ? -px[i] : px[i];
    }

}

void abs_int32(struct onnx_node_t *n){
  struct onnx_tensor_t *input = n->inputs[0];
  struct onnx_tensor_t *output = n->outputs[0];

  int8_t *px = (int32_t *)input->datas;
  int8_t *py = (int32_t *)output->datas;

  for (size_t i = 0; i < input->ndata; i++) {
    py[i] = px[i] < 0 ? -px[i] : px[i];
  }
}

void abs_f8(struct onnx_node_t *n){}
void abs_f16(struct onnx_node_t *n){}
void abs_f32(struct onnx_node_t *n){}