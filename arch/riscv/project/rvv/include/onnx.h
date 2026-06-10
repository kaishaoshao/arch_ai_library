#ifndef __MATH_RVV_ONNX_H
#define __MATH_RVV_ONNX_H

/// 定义枚举类型，表示ONNX张量的数据结构
enum onnx_tensor_type_t
{
    ONNX_TENSOR_TYPE_UNDEFINED = 0,
    ONNX_TENSOR_TYPE_BOOL = 9,
    ONNX_TENSOR_TYPE_INT8 = 3,
    ONNX_TENSOR_TYPE_INT16 = 5,
    ONNX_TENSOR_TYPE_INT32 = 6,
    ONNX_TENSOR_TYPE_INT64 = 7,
    ONNX_TENSOR_TYPE_UINT8 = 2,
    ONNX_TENSOR_TYPE_UINT16 = 4,
    ONNX_TENSOR_TYPE_UINT32 = 12,
    ONNX_TENSOR_TYPE_UINT64 = 13,
    ONNX_TENSOR_TYPE_BFLOAT16 = 16,
    ONNX_TENSOR_TYPE_FLOAT16 = 10,
    ONNX_TENSOR_TYPE_FLOAT32 = 1,
    ONNX_TENSOR_TYPE_FLOAT64 = 11,
    ONNX_TENSOR_TYPE_COMPLEX64 = 14,
    ONNX_TENSOR_TYPE_COMPLEX128 = 15,
    ONNX_TENSOR_TYPE_STRING = 8,
};

/// 定义结构体，表示ONNX张量
struct onnx_tensor_t {
    char *name;                     // 张量名称
    enum onnx_tensor_type_t type;   // 张量数据类型
    int *strides;                   // 张量的步长
    int *dims;                      // 张量的维度
    int ndim;                       // 张量维度数量
    void *datas;                    // 张量数据指针
    size_t ndata;                   // 张量数据数量
};

///  定义结构体，表示ONNX节点
struct onnx_node_t {
    struct onnx_tensor_t **inputs;  // 输入张量数组
    int ninput;                     // 输入张量数量
    struct onnx_tensor_t **outputs; // 输出张量数组
    int noutput;                    // 输出张量数量
    void *priv; // private data     // 私有数据
};

void abs_int8(struct onnx_node_t *n);
void abs_int16(struct onnx_node_t *n);
void abs_int32(struct onnx_node_t *n);
// void abs_int64(struct onnx_node_t *n);

void abs_f8(struct onnx_node_t *n);
void abs_f16(struct onnx_node_t *n);
void abs_f32(struct onnx_node_t *n);
// void abs_f64(struct onnx_node_t *n);

#endif // __MATH_RVV_ONNX_H
