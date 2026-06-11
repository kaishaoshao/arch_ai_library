OUTPUT_ARCH(riscv)
ENTRY(_start)

/*把内核放在0x80000000处*/
/*是RISC‑V QEMU virt 机器（以及许多真实 SiFive/StarFive 板子）默认的内核加载地址*/
SECTIONS
{
  . = 0x80000000;

  .text : {
    *(.text.entry) /*入口代码（通常来自 boot.S ) */
    *(.text*)      /*代码段*/
  }

  .rodata : { *(.rodata*) }  /*只读数据，如字符串常量、跳转表*/
  .data   : { *(.data*) }    /*已初始化的全局/静态变量*/
  .bss    : {                /*为初始化的全局变量*/
    /*脚本定义了 _bss_start 和 _bss_end 符号，供启动汇编代码在调用 C 函数前清零这片内存*/
    _bss_start = .;
    *(.bss*)
    *(COMMON)
    _bss_end = .;
  }
  /* 丢弃调试注释和异常处理帧信息， 减小内核体积并避免运行时多余段 */
  /DISCARD/ : { *(.comment*) *(.eh_frame) }

}

