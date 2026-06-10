import torch
import triton
import inspect
import triton_viz
from triton_viz.interpreter import record_builder


# puzzle:    :  待测试triton内核函数
# puzzle_spec:  待测试triton内核函数的spec
# nelem      ： 字典，定义问题的维度（如{"N0": 100, "N1": 200}）
# B          ： 字典，定义triton内核的块大小（如{"B0": 32, "B1": 64}）
# viz        ： 是否启用可视化调试（通过triton_viz）
def test(puzzle, puzzle_spec, nelem={}, B={"B0": 32}, viz=True):
    # 根据输入的 nelem自动填充缺失的块大小（B1、B2），默认值为 32
    B = dict(B)
    if "N1" in nelem and "B1" not in B:
        B["B1"] = 32
    if "N2" in nelem and "B2" not in B:
        B["B2"] = 32

    # 重制Triton可视化调试工具的记录器， 确保每次测试运行时从干净状态开始
    triton_viz.interpreter.record_builder.reset()
    # 设置随机数种子
    torch.manual_seed(0)
    
    # 获取函数签名, 解析的参数和返回值的维度信息
    signature = inspect.signature(puzzle_spec)
    args = {}
    for n, p in signature.parameters.items():
        print(p)
        args[n + "_ptr"] = ([d.size for d in p.annotation.dims], p)
    args["z_ptr"] = ([d.size for d in signature.return_annotation.dims], None)

    # 生成随机数据
    tt_args = []
    for k, (v, t) in args.items():
        tt_args.append(torch.rand(*v) - 0.5)
        if t is not None and t.annotation.dtypes[0] == "int32":
            tt_args[-1] = torch.randint(-100000, 100000, v)
    # 定义 Triton 内核的网格（Grid）​
    grid = lambda meta : (triton.cdiv(nelem["N0"], meta["B0"]),
                          triton.cdiv(nelem.get("N1", 1), meta.get("B1", 1)),
                          triton.cdiv(nelem.get("N2",1), meta.get("B2", 1)))

    # 运行 Triton 内核并验证结果​
    for k, v in args.items():
        print(k, v)
    triton_viz.trace(puzzle)[grid](*tt_args, **B, **nelem)
    z = tt_args[-1]
    tt_args = tt_args[:-1]
    z_ = puzzle_spec(*tt_args)
    match = torch.allclose(z, z_, rtol=1e-3, atol=1e-3)
    print("Result match:", match)
    # 错误处理和输出​
    failures = False
    if viz:
        failures = triton_viz.launch()
    if not match or failures:
        print("Invalid Access:", failures)
        print("Yours:", z)
        print("Spec:", z_)
        print(torch.isclose(z, z_))
        return

    from IPython.display import HTML
    import random
    print("Correct!")
    pups = [
    "2m78jPG",
    "pn1e9TO",
    "MQCIwzT",
    "udLK6FS",
    "ZNem5o3",
    "DS2IZ6K",
    "aydRUz8",
    "MVUdQYK",
    "kLvno0p",
    "wScLiVz",
    "Z0TII8i",
    "F1SChho",
    "9hRi2jN",
    "lvzRF3W",
    "fqHxOGI",
    "1xeUYme",
    "6tVqKyM",
    "CCxZ6Wr",
    "lMW0OPQ",
    "wHVpHVG",
    "Wj2PGRl",
    "HlaTE8H",
    "k5jALH0",
    "3V37Hqr",
    "Eq2uMTA",
    "Vy9JShx",
    "g9I2ZmK",
    "Nu4RH7f",
    "sWp0Dqd",
    "bRKfspn",
    "qawCMl5",
    "2F6j2B4",
    "fiJxCVA",
    "pCAIlxD",
    "zJx2skh",
    "2Gdl1u7",
    "aJJAY4c",
    "ros6RLC",
    "DKLBJh7",
    "eyxH0Wc",
    "rJEkEw4"]
    return HTML("""
    <video alt="test" controls autoplay=1>
        <source src="https://openpuppies.com/mp4/%s.mp4"  type="video/mp4">
    </video>
    """%(random.sample(pups, 1)[0]))




