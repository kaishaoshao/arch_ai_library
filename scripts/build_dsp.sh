# mkdir -p build && cd build
# cmake ../ -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -Qn -O3 -march=rv32imafdc -mabi=ilp32d -flto -DNDEBUG -fdata-sections -ffunction-sections \
#                      " -DCMAKE_CXX_FLAGS="  -Qn -O3 -flto -march=rv32imafdc -mabi=ilp32d -DNDEBUG -fdata-sections -ffunction-sections \
#                      "
# make -j10
rm build -rf
mkdir -p build
cd build
cmake ../ -DCMAKE_INSTALL_PREFIX=../output -DCOMPILER_REF_FUNCS=ON -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS="  -mcmodel=medlow -Qn -O2  -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d " -DCMAKE_CXX_FLAGS="-Qn -O2  -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d  -mcmodel=medlow " -G "Ninja"  && ninja install

# cmake ../ -DCMAKE_INSTALL_PREFIX=../output -DCOMPILER_REF_FUNCS=ON -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -Qn -O2  -flto  -fno-use-size-lib -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d " -DCMAKE_CXX_FLAGS="-Qn -O2 -fno-use-size-lib -flto -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d" -G "Ninja"  && ninja install

# cmake ../ -DCMAKE_INSTALL_PREFIX=../output  -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -Qn -O3 -flto  -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d " -DCMAKE_CXX_FLAGS="-Qn -O3 -flto  -DNDEBUG -fdata-sections -ffunction-sections -march=rv32imafdc_xxldsp -mabi=ilp32d" -G "Ninja"  && ninja install

# cmake ../ -DCMAKE_INSTALL_PREFIX=../output  -DCMAKE_C_COMPILER=zcc -DCMAKE_CXX_COMPILER=z++ -DCMAKE_C_FLAGS=" -O3   -march=rv32imafdc_xxldsp -mabi=ilp32d " -DCMAKE_CXX_FLAGS="-O3 -flto  -DNDEBUG  -march=rv32imafdc_xxldsp -mabi=ilp32d" -G "Ninja"  && ninja install

# -DRES_LOGN=10

