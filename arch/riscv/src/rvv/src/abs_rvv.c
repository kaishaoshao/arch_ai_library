#include "onnx-rvv.h"

// source form nuclei-ai-library
// only for study and test
void abs_rvv_int8(struct onnx_node_t *n){
  // 1. 初始化
  struct onnx_tensor_t *x = n->inputs[0];
  struct onnx_tensor_t *y = n->outputs[0];
  int8_t *py = (int8_t *)y->datas; // 输出数据指针
  int8_t *px = (int8_t *)x->datas; // 输入数据指针

  // 2. 循环设置
  size_t blkCnt = y->ndata; /* 循环计数器，即张量中的元素总数 */
  size_t vl;                // vl 将存储单次循环能处理的向量长度
  vint8m8_t vx, vy;         // 向量寄存器变量，用于存放 int8 数据

  // 3. 向量化主循环
  // __riscv_vsetvl_e8m8(blkCnt) 硬件的能力和剩余待处理元素数
  // blkCnt，来设置本次循环的向量长度v1
  // e8: 表示每个元素是8位的(element width)
  // m8: 表示向量寄存器分组(LMUL)，m8是最大分组，能提供最大的并行处理能力
  for (; (vl = __riscv_vsetvl_e8m8(blkCnt)) > 0; blkCnt -= vl) {
    // 4. 加载向量数据
    // i8: 表示输入数据的类型是8位整数
    // m8: 表示向量寄存器的分组大小
    vx = __riscv_vle8_v_i8m8(px, vl); // 从输入数据中加载向量
    px += vl; // 更新输入数据指针
    // 5. 创建掩码
    vbool1_t mask = __riscv_vmslt_vx_i8m8_b1(vx, 0); // 创建掩码，判断哪些元素小于0
    // 6. 计算绝对值
    vy = __riscv_vrsub_vx_i8m8_tumu(mask, vx, vx, 0, vl);
    // 7. 存储结果
    __riscv_vse8_v_i8m8(py, vy, vl); // 将结果存储到输出数据中
    py += vl; // 更新输出数据指针
    }
}

void abs_rvv_int32(struct onnx_node_t *n){
    struct onnx_tensor_t *x = n->inputs[0];
    struct onnx_tensor_t *y = n->outputs[0];
    int32_t *py = (int32_t *)y->datas;
    int32_t *px = (int32_t *)x->datas;

    size_t blkCnt = y->ndata; /* 循环计数器，即张量中的元素总数 */
    size_t vl;                // vl 将存储单次循环能处理的向量
    vint32m8_t vx, vy;         // 向量寄存器变量，用于存放 int32 数据

    for (; vl = __riscv_vsetvl_e32m8(blkCnt) > 0, blkCnt -= vl) {
      vx = __riscv_vsetvl_e32m8(px, vl);
      px += vl; // 更新输入数据指针
      vbool1_t mask = __riscv_vmslt_vx_i32m8_b4(vx, 0); // 创建掩码，判断哪些元素小于0
      vy = __riscv_vrsub_vx_i32m8_tumu(mask, vx, vx, 0, vl);
      __riscv_vse32_v_i32m8(py, vy, vl); // 将结果存储到输出数据中
      py += vl; // 更新输出数据指针
    }
}

void abs_rvv_f8(struct onnx_node_t *n){}
void abs_rvv_f16(struct onnx_node_t *n){}
void abs_rvv_f32(struct onnx_node_t *n){}
