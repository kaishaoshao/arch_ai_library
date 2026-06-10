import inspect
import ast

def jit(target="cpu"):
    assert target in ["cpu", "gpu","cuda"], "Invalid target"
    def inner(fn):
        # 返回JIT类的实例
        return JIT(fn, target=target)
    return inner

class JIT:
    def __init__(self, fn, target="cpu"):
        # 初始化时保存传入的函数
        self.fn = fn
        self.target = target

    def __call__(self, *args, **kwds):
        # 获取函数的源代码
        fn_src = inspect.getsource(self.fn)
        # 将源代码解析为抽象语法树（AST）
        fn_ast = ast.parse(fn_src)
        # 以可读格式打印AST
        print(ast.dump(fn_ast))

# 使用@jit装饰器装饰add函数
@jit(target="cpu")
def add():
    print("add")

# 调用add函数
add()