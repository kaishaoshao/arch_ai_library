import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 造波工厂：我们需要制造一杯“混合奶昔”
# ==========================================
def create_signal(N, Fs):
    t = np.arange(N) / Fs

    # 成分 A: 频率 5Hz，振幅 3.0
    signal_a = 3.0 * np.sin(2 * np.pi * 5 * t)

    # 成分 B: 频率 15Hz，振幅 1.0
    signal_b = 1.0 * np.sin(2 * np.pi * 15 * t)

    # 【叠加】：y[t] = a[t] + b[t]
    mixed_signal = signal_a + signal_b

    return t, mixed_signal, signal_a, signal_b

# ==========================================
# 2. 数学核心：暴力 DFT (离散傅里叶变换)
# 核心解释：频域的值是怎么算出来的？
# ==========================================
def slow_dft(signal):
    N = len(signal)
    dft_result = np.zeros(N, dtype=complex)

    # k 代表我们正在“试探”的频率 (0Hz, 1Hz, 2Hz...)
    for k in range(N):
        current_sum = 0 + 0j

        # 遍历信号的每一个时间点 n
        for n in range(N):
            # 1. 生成一个标准的“探测波”（旋转向量）
            # exp(-i * angle) = cos(angle) - i * sin(angle)
            angle = -2j * np.pi * k * n / N
            spin = np.exp(angle)

            # 2. 【核心步骤】：相乘 (Correlation)
            # 将 "你的信号" 与 "标准探测波" 相乘
            # 如果频率一致，乘积会很大（共振）；如果不一致，乘积会抵消。
            current_sum += signal[n] * spin

        # 3. 【核心步骤】：求和 (Integration)
        # 这个求和的结果，就是频域图上那个柱子的高度（复数形式）
        dft_result[k] = current_sum

    return dft_result

# ==========================================
# 3. 主程序
# ==========================================
N = 100      # 采样点数
Fs = 100     # 采样率

t, y, y_a, y_b = create_signal(N, Fs)

print("正在进行暴力计算 (DFT)...")
dft_output = slow_dft(y)

# 计算幅值并归一化
magnitude = np.abs(dft_output) / (N / 2)
magnitude[0] /= 2

freqs = np.arange(N) * (Fs / N)

# ==========================================
# 4. 绘图教学
# ==========================================
plt.figure(figsize=(14, 10))

# --- 图 1-3 (保持不变，展示时域叠加) ---
plt.subplot(3, 2, 1)
plt.plot(t, y_a, 'g--', alpha=0.7)
plt.title('1. Component A (5Hz)')
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 2)
plt.plot(t, y_b, 'm--', alpha=0.7)
plt.title('2. Component B (15Hz)')
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 3)
plt.plot(t, y, 'b-o', linewidth=2)
plt.title('3. Mixed Signal (Time Domain)')
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 4)
half_N = N // 2
plt.stem(freqs[:half_N], magnitude[:half_N])
plt.title('4. Frequency Domain (Result)')
plt.xlabel('Frequency (Hz)')
plt.grid(True, alpha=0.3)
plt.text(5, 2.5, '5Hz', color='red', ha='center')
plt.text(15, 1.2, '15Hz', color='red', ha='center')

# ==========================================
# 5. 新增：揭秘 DFT 内部是如何计算出值的？
# 原理：相关性 (Correlation) 分析
# ==========================================

# --- 场景 A：用 5Hz 的标准波去探测 (频率匹配 -> 共振) ---
# 生成纯 5Hz 的探测波 (为了画图只取实部 cos)
probe_5hz = np.cos(2 * np.pi * 5 * t)
# 相乘
product_5hz = y * probe_5hz
# 求和
sum_5hz = np.sum(product_5hz)

plt.subplot(3, 2, 5)
plt.plot(t, product_5hz, 'r-', alpha=0.8)
plt.fill_between(t, product_5hz, 0, color='red', alpha=0.2)
plt.title(f'5. Probing with 5Hz (MATCH!)\nSum of Area = {sum_5hz:.1f} (Large Value)')
plt.xlabel('Time')
plt.grid(True, alpha=0.3)

# --- 场景 B：用 10Hz 的标准波去探测 (频率不匹配 -> 抵消) ---
# 生成纯 10Hz 的探测波
probe_10hz = np.cos(2 * np.pi * 10 * t)
# 相乘
product_10hz = y * probe_10hz
# 求和
sum_10hz = np.sum(product_10hz)

plt.subplot(3, 2, 6)
plt.plot(t, product_10hz, 'k-', alpha=0.8)
plt.fill_between(t, product_10hz, 0, color='gray', alpha=0.2)
plt.title(f'6. Probing with 10Hz (MISMATCH)\nSum of Area = {sum_10hz:.1f} (Near Zero)')
plt.xlabel('Time')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()