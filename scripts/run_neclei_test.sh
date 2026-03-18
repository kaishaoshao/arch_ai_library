#!/bin/bash

# --- 环境与路径配置 ---
export NUCLEI_SDK_ROOT="/home/shaokai/Desktop/code/sdk/nuclei-sdk-terapines/"
export NUCLEI_SDK_NMSIS="/home/shaokai/Desktop/code/libml/DSP/NMSIS/NMSIS/"
export SOC=evalsoc
export PATH="/home/shaokai/Desktop/code/toolchains/nuclei-qemu-2025.02-linux-x64/qemu/bin:$PATH"
export PATH="/home/shaokai/Desktop/code/toolchains/nuclei_riscv_newlibc_prebuilt_linux64_2025.02/gcc/bin:$PATH"

sed -i "s/64K/512K/g" "$NUCLEI_SDK_ROOT/SoC/evalsoc/Board/nuclei_fpga_eval/Source/GCC/gcc_evalsoc_ilm.ld"
sed -i 's/\([ID]LM_MEMORY_SIZE\).*/\1 = 0x80000;/' "$NUCLEI_SDK_ROOT/SoC/evalsoc/Board/nuclei_fpga_eval/Source/GCC/evalsoc.memory"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
OUTPUT_FILE="$SCRIPT_DIR/output.txt"

# 强制切换到脚本所在目录
cd "$SCRIPT_DIR" || { echo "无法切换目录"; exit 1; }

TIMEOUT_DURATION="10s"
BASE_COMMAND="make SOC=evalsoc BOARD=nuclei_fpga_eval TOOLCHAIN=terapines NMSIS_LIB_COMPAT=1 DOWNLOAD=ilm CORE=n300fd ITERATIONS=1 SIMULATION=1 STDCLIB=newlib_nano RISCV_ARCH=rv32imafdc RISCV_ABI=ilp32d ARCH_EXT=xxldsp clean run_qemu"

# --- C 补丁内容 ---
PATCH_FAIL_OLD='        return 1;'
PATCH_FAIL_NEW='
#if defined(SIMULATION)
        *(volatile int*)0x100000 = 0x3333; /* Fail signal for QEMU */
#endif
        return 1;'
PATCH_SUCCESS_OLD='    return 0;'
PATCH_SUCCESS_NEW='
#if defined(SIMULATION)
    *(volatile int*)0x100000 = 0x5555; /* Pass signal for QEMU */
#endif
    return 0;'

# --- 主逻辑 ---
> "$OUTPUT_FILE"
echo "测试开始，日志文件: $OUTPUT_FILE" | tee -a "$OUTPUT_FILE"

# 核心修改：只遍历当前目录下的真实“文件夹”，彻底杜绝字符串解析错误
for dir in */; do
    # 去除目录名尾部的斜杠 (例如把 BasicMathFunctions/ 变成 BasicMathFunctions)
    dir="${dir%/}"

    # 防御：如果该目录下没有 Makefile，直接跳过
    if [ ! -f "$dir/Makefile" ]; then
        continue
    fi

    echo "========================================================================" | tee -a "$OUTPUT_FILE"
    echo "开始处理目录: '$dir'" | tee -a "$OUTPUT_FILE"

    # 使用原生 Bash 数组匹配 C 文件，不再用 find，防止被终端转义字符干扰
    main_c_file=""
    match_count=0

    for c_file in "$dir"/*.c; do
        # 确保真的找到了 .c 文件（处理目录内没 C 文件时的通配符异常）
        if [ -f "$c_file" ]; then
            # -q 静默输出，-w 精准匹配独立单词 "main"
            if grep -qw "main" "$c_file"; then
                main_c_file="$c_file"
                match_count=$((match_count + 1))
            fi
        fi
    done

    if [ $match_count -eq 0 ]; then
        echo "警告: 在 '$dir' 中未找到包含 'main' 的 C 文件。跳过。" | tee -a "$OUTPUT_FILE"
        continue
    elif [ $match_count -gt 1 ]; then
        echo "警告: 在 '$dir' 中找到 $match_count 个包含 'main' 的文件。跳过以策安全。" | tee -a "$OUTPUT_FILE"
        continue
    fi

    echo "找到主文件: $main_c_file" | tee -a "$OUTPUT_FILE"
    backup_file="${main_c_file}.bak"

    {
        echo "  -> 正在创建备份..."
        cp "$main_c_file" "$backup_file"

        echo "  -> 正在应用补丁..."
        if grep -q "0x3333" "$main_c_file"; then
            echo "    -> 补丁已存在，跳过。"
        else
            sed -i "s|$PATCH_FAIL_OLD|$PATCH_FAIL_NEW|g" "$main_c_file"
            sed -i "s|$PATCH_SUCCESS_OLD|$PATCH_SUCCESS_NEW|g" "$main_c_file"
        fi

        echo "  -> 正在执行测试 (超时时间: $TIMEOUT_DURATION)..."
        (
            cd "$dir" && timeout "$TIMEOUT_DURATION" $BASE_COMMAND
        )
        status=$?

        if [ $status -eq 124 ]; then
            echo "结果: 在 '$dir' 中的测试超时 (TIMEOUT)。"
        elif [ $status -ne 0 ]; then
            echo "结果: 在 '$dir' 中的测试失败，退出码: $status."
        else
            echo "结果: 在 '$dir' 中的测试成功 (SUCCESS)."
        fi

    } | tee -a "$OUTPUT_FILE"

    if [ -f "$backup_file" ]; then
        echo "  -> 正在恢复备份..." | tee -a "$OUTPUT_FILE"
        mv "$backup_file" "$main_c_file"
    fi
    echo "" | tee -a "$OUTPUT_FILE"
done

echo "========================================================================" | tee -a "$OUTPUT_FILE"
echo "所有测试已完成。" | tee -a "$OUTPUT_FILE"