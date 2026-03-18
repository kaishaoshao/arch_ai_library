export NUCLEI_SDK_ROOT=/home/shaokai/Desktop/code/sdk/nuclei-sdk
export NUCLEI_SDK_NMSIS=/home/shaokai/Desktop/code/DSP/NMSIS/NMSIS/
export SOC=evalsoc
export PATH=/home/shaokai/Desktop/code/toolchains/nuclei-qemu-2025.02-linux-x64/qemu/bin:$PATH
sed -i "s/64K/512K/g" $NUCLEI_SDK_ROOT/SoC/evalsoc/Board/nuclei_fpga_eval/Source/GCC/gcc_evalsoc_ilm.ld
# For Nuclei SDK >= 0.7.0
sed -i 's/\([ID]LM_MEMORY_SIZE\).*/\1 = 0x80000;/' $NUCLEI_SDK_ROOT/SoC/evalsoc/Board/nuclei_fpga_eval/Source/GCC/evalsoc.memory
make SOC=evalsoc BOARD=nuclei_fpga_eval TOOLCHAIN=terapines      DOWNLOAD=ilm CORE=n300fd ITERATIONS=1 SIMULATION=1   STDCLIB=newlib_nano RISCV_ARCH=rv32imafdc_xxldsp RISCV_ABI=ilp32d clean run_qemu
