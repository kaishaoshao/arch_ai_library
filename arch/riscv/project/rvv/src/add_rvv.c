void add_f16(struct onnx_node_t *n){
    //  1.初始化
    struct onnx_tensor_t *x = n->inputs[0];
    struct onnx_tensor_t *y = n->outputs[0];
    struct onnx_tensor_t *z = n->inputs[1];

    float16_t *px = (float16_t *)x->datas; // 输入数据指针
    float16_t *py = (float16_t *)y->datas; // 输出数据指针
    float16_t *pz = (float16_t *)z->datas; // 第二个输入数据指针

    for (size_t i = 0, l = y->ndata; i < l; i++)
    {
        py[i] = px[i] + pz[i]; // 执行加法操作
    }


}