# SIMD Loops

## Introduction
SIMD Loops is a collection of self-contained, real-world loop kernels — written in a mix of C, ACLE intrinsics, and inline assembly — that target everything from simple arithmetic to matrix multiplication, sorting, and string processing. You can compile them, run them, step through them, and use them as a foundation for your own SIMD work. The goal of this project is to help you learn to write SIMD code for modern Arm architectures through working, readable examples that demonstrate how to use the full range of features available in SVE (Scalable Vector Extension) and SME (Scalable Matrix Extension). Each example is a self-contained loop kernel – a small piece of code that performs a specific task and shows how that task can be implemented across different vector instruction sets.

The available loops are documented [here](loops/loops.md).

## License Information
This project is licensed under the [BSD 3-Clause License](LICENSE.md).

## How to Build

### Prerequisites
SIMD Loops supports the native AArch64/Linux Clang toolchain by default. The compiler target is typically represented as `aarch64-unknown-linux-gnu` or `aarch64-none-linux-gnu`, and you can check this by simply running `clang` with the `--version` flag. However, it is possible to tweak Makefile variables to support other toolchains as long as they are compatible.

### Build Targets
SIMD Loops supports several build targets, each focusing on a certain technology and/or version of a technology. It is expected that the toolchain used supports the build target one chooses. Similarly, the machine is expected to have the necessary support to run.

The following is the list of build targets supported by SIMD Loops:

| Build Target       | Description                                                           |
|:-------------------|:----------------------------------------------------------------------|
| c-scalar           | Build the C version of the loops but disable vector code generation   |
| scalar             | Build the scalar assembly variant of the loops                        |
| autovec-sve        | Build the C version of the loops with SVE auto-vectorization enabled  |
| autovec-sve2       | Build the C version of the loops with SVE2 auto-vectorization enabled |
| neon               | Build the Neon assembly variant of the loops                          |
| sve                | Build the SVE assembly variant of the loops                           |
| sve2               | Build the SVE2 assembly variant of the loops                          |
| sme2               | Build the SME2 assembly variant of the loops                          |
| sme-ssve           | Build the streaming SVE assembly variant of the loops                 |
| sve2p1             | Build the SVE2p1 assembly variant of the loops                        |
| sme2p1             | Build the SME2p1 assembly variant of the loops                        |
| sve-intrinsics     | Build the SVE2 ACLE intrinsics variant of the loops                   |
| sme-intrinsics     | Build the SME2 ACLE intrinsics variant of the loops                   |

### Build Environment
If the toolchain binaries are not available in the `PATH`, then you can set the following environment variables:

1. `C_COMPILER` → path to compiler binary (including the name).
2. `OBJDUMP` → path to the objdump binary (including the name).

#### Example:
```bash
export C_COMPILER=/path/to/bin/clang
export OBJDUMP=/path/to/bin/llvm-objdump
```

### Build Invocation
Once the environment is set, and assuming the current working directory is `simd-loops/`, you can build all the build targets using:
```bash
make all
```

Or selectively, using:
```bash
make <make-target>
```

#### Example:
```bash
make sve2p1
```

To know all the build targets available, you can simply run `make` without any argument. This will result in an error followed by a list of all available targets.

#### Example:
```bash
make
ERROR: Makefile target not specified. Please use one of the following targets:
all fmt clean c-scalar scalar autovec-sve autovec-sve2 neon sve sve2 sme2 sme-ssve sve2p1 sme2p1 sve-intrinsics sme-intrinsics
```

To clean the build directory, you can simply do:
```bash
make clean
```

## Build Output
```
simd-loops/build/<make-target>
  |
  +- bin/
  |   |
  |   +- simd_loops            // executable binary (all loops)
  |
  +- dis/
  |   |
  |   +- simd_loops.objdump    // disassembly of 'simd_loops'
  |
  +- standalone/
  |   |
  |   +- bin/
  |       |
  |       +- loop_*.elf        // standalone executable binary for each loop
  |
  +- _obj/                     // temporary build files
  |
  *
```

## How to Run
A loop can be run by executing the combined binary or the standalone executable. In both cases, a `Checksum correct.` message is printed once the execution completes successfully.

### Using the Combined Binary Executable
```bash
./build/<target>/bin/simd-loops -k <loop-number> -n <number-of-iterations>
```

#### Example:
```bash
./build/<target>/bin/simd-loops -k 1 -n 2
Loop 001 - fp32 FMA
 - Purpose: Use of fp32 FMA
 - Checksum correct.
```

### Using the Standalone Executable
```bash
./build/<target>/standalone/bin/loop_<loop-number>.elf
```

### Note
Not all targets are supported for all the loops. If a target is not supported, then the following message will be printed:
```bash
ABORT: No implementations available for this target.
```
---
