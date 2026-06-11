cmake_minimum_required(VERSION 3.31)

set(CMAKE_C_COMPILER "/home/shaokai/Terapines/ZCC/4.1.9/bin/zcc")
set(CMAKE_ASM_COMPILER "/home/shaokai/Terapines/ZCC/4.1.9/bin/zcc")
project(miniOS C ASM)

set(CMAKE_C_STANDARD 11)


add_subdirectory(src)

set(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/src/arch/riscv/linker.ld)

add_executable(miniOS.elf ${CMAKE_SOURCE_DIR}/src/boot/main.c ${LINKER_SCRIPT})
set_target_properties(miniOS.elf PROPERTIES LINK_DEPENDS ${LINKER_SCRIPT} LINKER_LANGUAGE C)
target_link_options(miniOS.elf PRIVATE -T ${LINKER_SCRIPT})
target_link_libraries(miniOS.elf PRIVATE
    miniOS-boot
    miniOS-drivers
)
