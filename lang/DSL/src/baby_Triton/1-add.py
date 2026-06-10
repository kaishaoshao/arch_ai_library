def jit(fn):
    def inner():
        print("jit is called")
    return inner

@jit
def add():
    print("add")

add()
