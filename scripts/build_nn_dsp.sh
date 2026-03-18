# mkdir -p build && cd build
# cmake ../ -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -Qn -O3 -march=rv32imafdc -mabi=ilp32d -flto -DNDEBUG -fdata-sections -ffunction-sections \
#                      " -DCMAKE_CXX_FLAGS="  -Qn -O3 -flto -march=rv32imafdc -mabi=ilp32d -DNDEBUG -fdata-sections -ffunction-sections \
#                      "
# make -j10
mkdir -p build
cd build
cmake ../ -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -O2 -flto -march=rv32imafdc_xxldspn2x -mabi=ilp32d" -DCMAKE_CXX_FLAGS="-O2 -flto -march=rv32imafdc_xxldspn2x -mabi=ilp32d" -G "Ninja" && ninja

# -DRES_LOGN=10
