# cuda_study

参考 权双大佬的视频 [B站链接](https://www.bilibili.com/video/BV1sM4y1x7of?p=6&vd_source=2cb22062bbd1ad0823747ec35d88c863)

## 后缀

.cu 后缀包含 cpp程序和cuda程序

## 核函数

* 核函数在GPU上进行并行执行
* 注意：

  * 限定词__global__修饰
  * 返回值必须是void
  * 不支持C++的iostream
* 形式 见 hello.cu

  * hello_from_gpu<<<3,1>>>();

      核函数调用  1.线程块数量 2.线程块里面线程数量
* 注意事项

  * 核函数只能当问GPU内存
  * 核函数不能使用变长参数
  * 核函数不能使用静态变量
  * 核函数不能使用函数指针
  * 核函数具有异步性


## 线程模型
