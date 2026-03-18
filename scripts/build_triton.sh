export DEBUG=1
export LLVM_BUILD_DIR=/home/shaokai/Desktop/code/llvm/workpace/spirv/triton-spirv/llvm-project-for-ztc/build
export MLIR_DIR="/home/shaokai/Desktop/code/llvm/workpace/spirv/triton-spirv/llvm-project-for-ztc/build/lib/cmake/mlir"
export CMAKE_PREFIX_PATH="/home/shaokai/Desktop/code/llvm/workpace/spirv/triton-spirv/llvm-project-for-ztc/build"
pip install -r python/requirements.txt
LLVM_INCLUDE_DIRS=$LLVM_BUILD_DIR/include \
LLVM_LIBRARY_DIR=$LLVM_BUILD_DIR/lib \
LLVM_SYSPATH=$LLVM_BUILD_DIR \
pip install -e  . --no-build-isolation