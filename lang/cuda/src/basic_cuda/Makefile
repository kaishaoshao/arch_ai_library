NVCC = nvcc
CC   = gcc

# 编译器与架构自动检测
ARCH := $(shell $(NVCC) -run ./detect_arch.cu 2>/dev/null || echo "sm_75")

# OpenCL设置
OPENCL_LIBS     := $(shell pkg-config --libs OpenCL 2>/dev/null || echo "-lOpenCL")
OPENCL_INCLUDES := $(shell pkg-config --cflags OpenCL 2>/dev/null || echo "")

# -Xcompiler -Wno-error : 忽略编译器警告
# --no-device-link      : 表示编译时跳过设备代码的链接步骤，通常用于编译将被动态加载的代码
#                         或者当你在构建不需要可重定位设备代码的独立对象文件时使用。
# -lcupti -lnvToolsExt  : 用于链接NVIDIA Profiling Tools Interface 和 NVTX (用于代码插桩和性能分析)
# -ldl -lpthread        : 用于动态链接库和多线程支持

# NVCC FLAGS
NVCC_FLAGS      = -O3 -arch=$(ARCH) -Xcompiler -Wno-error --no-device-link
NVCC_DP_FLAS    = -O3 -arch=$(ARCH) -Xcompiler -Wno-error --no-device-link
NVCC_PROF_FLAGS = -O3 -arch=$(ARCH) -Xcompiler -Wno-error --no-device-link -lcupti -lnvToolsExt
NVCC_EXT_FLAGS  = -O3 -arch=$(ARCH) -Xcompiler -Wno-error --no-device-link -ldl -lpthread
NVCC_PTX_FLAGS  = -std=c++11 -arch=$(ARCH) -Xcompiler -Wno-error --no-device-link

# OpenCL FLAGS
OPENCL_FLAGS = -O3 -std=c11

.PHONY: all clean detect_arch ptx-demos

all: detect_arch 01-vector-add 01-homework

ptx-dems:

detect_arch:
	@echo "Detected GPU architecture: $(ARCH)"
	@if [ "$(ARCH)" = "sm_61" ]; then \
		echo "Using default sm_61 architecture. To use actual GPU architecture:"; \
		echo "1. Create detect_arch.cu with the code to detect architecture"; \
		echo "2. Or manually set architecture in Makefile"; \
	fi

01-vector-add: 01-vector-add.cu
	$(NVCC) $(NVCC_FLAGS) 01-vector-add.cu -o 01-vector-add.out

01-homework: ./homework/01-FMA.cu 
	$(NVCC) $(NVCC_FLAGS) ./homework/01-FMA.cu -o 01-FMA.out



clean:
	rm -f *.out
