rust学习路线

## cargo

创建项目

```
$ cargo new world_hello
$ cd world_hello
```

## rust基本概念

* 所有权、借用、生命周期
* 宏编程
* 模式匹配
*

## 基础语法

* pub关键字

| 关键字         | 可见范围   | 说明                 |
| -------------- | ---------- | -------------------- |
| （无）         | 当前模块   | 默认私有             |
| `pub`          | 任何地方   | 完全公开             |
| `pub(crate)`   | 当前 crate | 同包内可见           |
| `pub(super)`   | 父模块     | 上级模块可见         |
| `pub(self)`    | 当前模块   | 等同于默认（显式写） |
| `pub(in path)` | 指定路径   | 特定模块可见         |

* as usize : 转化为平台相关无符号





## rustlings

### 环境准备

下载

```
cargo install rustlings
```

初始化

```
rustlings init my-rustlings
```

练习

```
rustlings run  xxx   # 运行当前练习
rustlings check-all  # 验证所有练习
```

练习类型

```
exercises/
├── variables/          # 变量绑定
├── functions/          # 函数
├── if/                 # 条件语句
├── primitive_types/    # 基本类型
├── vecs/               # 向量
├── move_semantics/     # 所有权和移动语义
├── structs/            # 结构体
├── enums/              # 枚举
├── strings/            # 字符串
├── modules/            # 模块系统
├── hashmaps/           # 哈希映射
├── options/            # Option 类型
├── error_handling/     # 错误处理
├── generics/           # 泛型
├── traits/             # 特性
├── tests/              # 测试
├── lifetimes/          # 生命周期
├── iterators/          # 迭代器
├── threads/            # 并发
└── smart_pointers/     # 智能指针
```

* rust需要指定具体类型： i32
* rust默认值是不可变的， 需要mut,才可以修改值
* Shadowing vs Mutability

| 特性     | `mut`      | Shadowing (`let`) |
| :------- | :----------- | :------------------ |
| 修改值   | ✅ 可以      | ❌ 创建新变量       |
| 改变类型 | ❌ 不可以    | ✅ 可以             |
| 内存安全 | 同一内存位置 | 新分配内存          |

* rust函数声明也需要指定具体的数据类型
* rust函数如果被使用，则必须提供返回类型
* rust只用函数类型声明时才使用分号
* Rust Range 语法规则 `[start..end]` 是**左闭右开**区间（包含 start，不包含 end）：

| 写法          | 含义                 | 结果                |
| :------------ | :------------------- | :------------------ |
| `&a[1..3]`  | 索引 1 到 2（不含3） | `[2, 3]`          |
| `&a[1..4]`  | 索引 1 到 3（不含4） | `[2, 3, 4]` ✅    |
| `&a[0..=2]` | 索引 0 到 2（含2）   | `[1, 2, 3]`       |
| `&a[..]`    | 全部                 | `[1, 2, 3, 4, 5]` |
