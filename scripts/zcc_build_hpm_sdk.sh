#!/bin/bash
# demo名称
demo="samples/hpm_math/rfft"

# samples/opener/motor
# samples/microros/publisher
# samples/microros/service

# 脚本目录
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
echo "hpm_sdk directory: $SCRIPT_DIR"
export HPM_SDK_BASE=$SCRIPT_DIR

# zcc安装目录
# ZCC_INSTALL_DIR=$(zcc -v 2>&1 | grep "InstalledDir" | awk '{print $2}')
ZCC_INSTALL_DIR=/home/shaokai/Downloads/zcc-linux-master-build14281-pro/install-zcc-pro/bin
# ZCC_INSTALL_DIR=/opt/zcc-toolchain/3.2.5/bin


# echo "zcc install directory: $ZCC_INSTALL_DIR"
export GNURISCV_TOOLCHAIN_PATH=$ZCC_INSTALL_DIR/../
export HPM_SDK_TOOLCHAIN_VARIANT=zcc

# 环境变量
source "$SCRIPT_DIR/env.sh"

# 构建目录
BUILD_DIR="$SCRIPT_DIR/$demo/build_4.1.4"
if [ $1=="-c" ]; then
    echo "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
else
    echo "Build completed successfully."
fi

if [ $1=="-all" ]; then
    cd samples && mkdir -p build  && cd build
    echo "Current directory: $(pwd)"
    for i in `find .. -name  CMakeLists.txt`;
    do rm * -rf;
        cmake -GNinja -DBOARD=hpm6750evk2 $(dirname $i)  -DHPM_BUILD_TYPE=flash_xip_release;
        ninja;
    done > ~/Downloads/hpm_sdk——16——0.log 2>&1
else
   mkdir -p "$BUILD_DIR"
   cmake -DCMAKE_C_FLAGS="-Os " \
         -GNinja -DBOARD=hpm5300evk \
         -S "$SCRIPT_DIR/$demo" -B "$BUILD_DIR" &&   ninja -C "$BUILD_DIR"
fi


# samples/motor_ctrl/bldc_over_zero
# hpm_sdk/samples/vglite/tiger

