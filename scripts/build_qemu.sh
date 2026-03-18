#!/bin/bash

# 创建构建目录
mkdir -p build
cd build || exit 1

# 设置安装前缀
prefix=$(pwd)/qemu

# 根据传入参数设置目标架构
if [ "$1" = "riscv64" ]; then
    targets="riscv64-softmmu,riscv64-linux-user"
elif [ "$1" = "riscv32" ]; then
    targets="riscv32-softmmu,riscv32-linux-user"
else
    # 默认构建所有RISC-V目标
    targets="riscv64-softmmu,riscv64-linux-user,riscv32-softmmu,riscv32-linux-user"
fi

# 运行配置
../configure \
    --target-list="$targets" \
    --disable-werror \
    --prefix="$prefix" \
    --enable-debug

# 编译
make -j$(nproc)