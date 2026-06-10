import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. 配置参数
# ==========================================
C_SOURCE_FILE = "simple_fft.c"
EXECUTABLE = "fft_program"
if os.name == 'nt': # Windows系统
    EXECUTABLE += ".exe"

N = 64          # FFT 点数 (必须是 2 的幂)
Fs = 1000       # 采样率 (Hz) - 就像每秒钟拍1000张照片

# ==========================================
# 2. 生成模拟信号 (Python)
# ==========================================
# 时间轴：0 到 N/Fs 秒
t = np.arange(N) / Fs

# 生成信号：我们故意混合两个频率
# 1. 主波：50Hz，振幅 1.0
# 2. 次波：120Hz，振幅 0.5
freq1 = 50
amp1 = 1.0
freq2 = 120
amp2 = 0.5

signal = amp1 * np.sin(2 * np.pi * freq1 * t) + \
         amp2 * np.sin(2 * np.pi * freq2 * t)

# 准备发送给 C 程序的数据字符串
# 格式：第一行是 N，后面跟随 N 个数据点
input_data_str = f"{N}\n" + "\n".join(map(str, signal))

# ==========================================
# 3. 调用 C 程序进行计算
# ==========================================
print(f"正在编译 {C_SOURCE_FILE}...")
compile_cmd = ["gcc", C_SOURCE_FILE, "-o", EXECUTABLE, "-lm"]
compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

if compile_result.returncode != 0:
    print("编译失败！请检查是否安装了 GCC。")
    print(compile_result.stderr)
    exit(1)

print("正在运行 C 程序进行 FFT 计算...")
# 使用 subprocess 管道传输数据：Python -> C -> Python
process = subprocess.run(
    [f"./{EXECUTABLE}"],
    input=input_data_str,
    text=True,
    capture_output=True
)

if process.returncode != 0:
    print("C 程序运行出错！")
    print(process.stderr)
    exit(1)

# ==========================================
# 4. 解析 C 程序的输出
# ==========================================
output_lines = process.stdout.strip().split('\n')
fft_result_c = []

for line in output_lines:
    try:
        # C 程序输出格式为: "real imag"
        parts = line.split()
        if len(parts) >= 2:
            real = float(parts[0])
            imag = float(parts[1])
            fft_result_c.append(complex(real, imag))
    except ValueError:
        continue

fft_result_c = np.array(fft_result_c)

# 计算幅值 (Magnitude) 并归一化
# FFT的原始结果如果不除以 N/2，数值会很大，不直观
# 除以 N/2 后，幅值就会接近我们在代码里设置的 amp1 (1.0) 和 amp2 (0.5)
# 注意：直流分量(DC)应该除以 N，这里为了简化只处理交流分量
magnitude = np.abs(fft_result_c) / (N / 2)
magnitude[0] = magnitude[0] / 2 # DC分量单独处理

# 计算频率轴 (X轴的刻度)
freqs = np.fft.fftfreq(N, 1/Fs)

# 只需要显示前半部分（正频率）
half_n = N // 2
freqs_half = freqs[:half_n]
magnitude_half = magnitude[:half_n]

# ==========================================
# 5. 绘图 (Matplotlib)
# ==========================================
plt.figure(figsize=(12, 8))

# --- 图 1: 时域信号 ---
plt.subplot(2, 1, 1)
plt.plot(t, signal, 'b.-', label='Mixed Signal')
plt.title(f'Time Domain (Input): A messy wave\n(50Hz + 120Hz mixed)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)
plt.legend()

# --- 图 2: 频域结果 ---
plt.subplot(2, 1, 2)
# 使用 stem 画火柴杆图，这最适合看离散频率
markerline, stemlines, baseline = plt.stem(freqs_half, magnitude_half)
plt.setp(stemlines, 'linewidth', 1.5)

plt.title('Frequency Domain (Output): The "Ingredients List"\nLook for the tall bars!')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (Approx. Amplitude)')
plt.grid(True, alpha=0.3)
plt.xlim(0, 200) # 只显示 0-200Hz，方便观察

# 自动标注峰值
for x, y in zip(freqs_half, magnitude_half):
    if y > 0.1: # 只标注比较明显的峰值 (忽略噪音)
        plt.annotate(f"{x:.0f}Hz\n(Amp:{y:.1f})",
                     xy=(x, y),
                     xytext=(0, 10),
                     textcoords="offset points",
                     ha='center',
                     fontsize=10,
                     fontweight='bold',
                     color='red')

plt.tight_layout()
plt.show()

print("完成！请查看弹出的图表。")
print(f"预期看到：在 50Hz 处有个高柱子 (约1.0)，在 120Hz 处有个矮柱子 (约0.5)。")