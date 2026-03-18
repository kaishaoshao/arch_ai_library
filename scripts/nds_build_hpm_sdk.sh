#!/bin/bash
# demo名称
demo="samples/hello_world"

# 脚本目录
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
echo "hpm_sdk directory: $SCRIPT_DIR"
export HPM_SDK_BASE=$SCRIPT_DIR

# adsgcc安装目录
ADSGCC_INSTALL_DIR=/share/rd/toolchain/Andestech/AndeSight_STD_v533/toolchains/nds32le-elf-mculib-v5/bin/

echo "adsgcc install directory: $ADSGCC_INSTALL_DIR"
export GNURISCV_TOOLCHAIN_PATH=$ADSGCC_INSTALL_DIR/../
export HPM_SDK_TOOLCHAIN_VARIANT=nds-gcc

# 环境变量
source "$SCRIPT_DIR/env.sh"

# 构建目录
BUILD_DIR="$SCRIPT_DIR/$demo/build_5300"

mkdir -p "$BUILD_DIR"
cmake -DCMAKE_C_FLAGS="-v" \
      -GNinja -DBOARD=hpm5300evk \
      -S "$SCRIPT_DIR/$demo" -B "$BUILD_DIR" && \
ninja -C "$BUILD_DIR" -j8
