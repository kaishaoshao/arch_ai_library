import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 造波工厂：我们需要制造一杯“混合奶昔”
# ==========================================
def create_signal(N, Fs):
    t = np.arange(N) / Fs
    # 这是一个混合信号：
    # 成分 A: 频率 5Hz，振幅 3.0
    # 成分 B: 频率 15Hz，振幅 1.0
    signal = 3.0 * np.sin(2 * np.pi * 5 * t) + \
             1.0 * np.sin(2 * np.pi * 15 * t)
    return t, signal

# ==========================================
# 2. 数学核心：暴力 DFT (离散傅里叶变换)
# 这是最原始的算法，虽然慢，但逻辑最清楚
# ==========================================
def slow_dft(signal):
    N = len(signal)
    # 准备一个空的复数数组存放结果（这就是那张“食谱”）
    dft_result = np.zeros(N, dtype=complex)

    # --- 外层循环：遍历每一个可能的频率 k ---
    # 我们要试探从 0 到 N-1 的每一个频率
    for k in range(N):
        current_sum = 0 + 0j

        # --- 内层循环：计算“共振” ---
        # 对于当前的频率 k，我们遍历信号的每一个点 n
        for n in range(N):
            # 欧拉公式：e^(-i * 2*pi * k * n / N)
            # 这就是一个在复平面上旋转的单位圆
            # 简单理解：这就相当于生成了一个频率为 k 的“探测波”
            angle = -2j * np.pi * k * n / N
            spin = np.exp(angle)

            # 将原信号与探测波相乘，并累加
            current_sum += signal[n] * spin

        dft_result[k] = current_sum

    return dft_result

# ==========================================
# 3. 主程序
# ==========================================
# 设置参数
N = 100      # 采样点数
Fs = 100     # 采样率 (100Hz)

# 1. 获取时间轴和混合信号
t, y = create_signal(N, Fs)

# 2. 执行变换 (这里我们用自己写的 slow_dft，而不是 numpy.fft)
print("正在进行暴力计算 (DFT)...")
dft_output = slow_dft(y)

# 3. 计算幅值 (Magnitude)
# 复数结果包含实部和虚部，我们需要计算它的模长：sqrt(real^2 + imag^2)
# 归一化：除以 N/2 才能得到真实的物理振幅
magnitude = np.abs(dft_output) / (N / 2)
magnitude[0] /= 2 # 直流分量特殊处理

# 4. 计算频率轴 (X轴)
# 生成 0, 1, 2... 对应的真实频率 Hz
freqs = np.arange(N) * (Fs / N)

# ==========================================
# 4. 绘图教学
# ==========================================
plt.figure(figsize=(12, 8))

# 图 1: 时域 (Time Domain) - 这就是“奶昔”
plt.subplot(2, 1, 1)
plt.plot(t, y, 'b-o', label='Mixed Signal')
plt.title('1. Time Domain: What we hear/measure (The Smoothie)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)
plt.legend()

# 图 2: 频域 (Frequency Domain) - 这就是“食谱”
plt.subplot(2, 1, 2)
# 只画前一半 (N/2)，因为结果是对称的
half_N = N // 2
plt.stem(freqs[:half_N], magnitude[:half_N])

plt.title('2. Frequency Domain: The Recipe List (DFT Result)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)

# 标注我们找到的成分
plt.text(5, 2.5, 'Found: 5Hz (Amp=3)', color='red', ha='center')
plt.text(15, 1.2, 'Found: 15Hz (Amp=1)', color='red', ha='center')

plt.tight_layout()
plt.show()