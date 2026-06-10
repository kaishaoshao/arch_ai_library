import inspect
import ast

def jit(target="cpu"):
    assert target in ["cpu", "gpu", "cuda"], "Invalid target"
    def inner(fn):
        # 返回JIT类的实例
        return JIT(fn, target=target)
    return inner

class JIT:
    def __init__(self, fn, target):
        # 初始化时保存传入的函数和目标
        self.fn = fn
        self.target = target

    def __call__(self, *args, **kwds):
        # 获取函数的源代码
        fn_src = inspect.getsource(self.fn)
        # 将源代码解析为抽象语法树（AST）
        fn_ast = ast.parse(fn_src)
        # 以可读格式打印AST
        print(ast.dump(fn_ast))
        
        # 创建代码生成器实例并生成代码
        code_generator = CodeGenerator(fn_ast, self.target)
        code_generator.code_gen()

class CodeGenerator(ast.NodeVisitor):
    def __init__(self, fn_ast, target):
        # 初始化时保存传入的AST和目标
        self.fn_ast = fn_ast
        self.target = target

    def code_gen(self):
        # 生成代码时访问AST
        self.visit(self.fn_ast)

    def visit(self, node):
        # 访问AST节点时打印节点类型
        print("Visit ---> " + node.__class__.__name__)
        return super().visit(node)

# 使用@jit装饰器装饰add函数
@jit(target="cpu")
def add():
    print("add")

# 调用add函数
add()