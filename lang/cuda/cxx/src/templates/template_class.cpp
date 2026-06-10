// <> 空的尖括号表示这个是特化版本
// template <>
// 为float提供特殊实现
// class Tensor<float> {
// };

// 为什么要使用模版特化 ？
// 1.为特定类型提供优化实现
// 通用模版
// template <typename T>
// class Tensor {
// 通用实现
// };
// 为float类型特化(可能使用SIMD)指令
// template <>
// class Tensor<float> {
  // 针对float的高度优化实现
  // 比如使用SSE/AVX指令集
// };

// 2.处理特殊类型的行为
// template <typename T>
// class Serializer {
//   void serialize(const T &data) {
//     // 通用序列化
//    }
// };

// 维string类型特化
// template <>
// class Serializer<std::string> {
//   void serialize(const std::string &str) {
//       // 针对string的特殊序列化逻辑
//   }
// };


#include <iostream>
#include <chrono>

// arm
#ifdef __ARM_NEON__
#include <arm_neon.h>
#elif __X86_AVX__
#include <immintrin.h>
else

#endif // __ARM_NEON__ || __X86__

// 通用模版 - 普通实现
template <typename T>
class VectorProcessor {
public:
  static void addArrays(T *a, T *b, T *result, int size) {
    std::cout << "通用版本";
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < size; ++i)
      result[i] = a[i] + b[i];
    auto end = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "耗时" << duration.count() << "微秒\n";
  }
};

// 为float类型特化 - 使用SIMD指令集优化
template <> class VectorProcessor<float> {
public:
  static void addArrays(float *a, float *b, float *result, int size) {
    std::cout << "float 特化版本(SIMD优化):";
    auto start = std::chrono::high_resolution_clock::now();

    // SIMD 一次取8个指令
    int i = 0;

#ifdef __ARM_NEON__
    for(; i <= size - 4; i+=4) {
      float32x4_t vecA = vld1q_f32(a + i);  // 加载4个float
      float32x4_t vecB = vld1q_f32(b + i);
      float32x4_t vecResult = vaddq_f32(vecA, vecB);
      vst1q_f32(result + i, vecResult);
    }
#elif __X86_AVX__
    for(; i <= size - 4; i+=4) {
      _m128 vevA = _mm128_loadu_ps(a + i);
      _m128 vecB = _mm128_loadu_ps(b + i);
      _m128 vecResult = _mm128_add_ps(vecA, vecB);
      _mm128_storeu_ps(result + i, vecResult);
    }
    // 处理剩余元素
    for (; i < size; i++) {
      result[i] = a[i] + b[i];
    }
#else
  std::cout << "[SIMD不可用, 使用普通实现]\n"
#endif // __ARM_NEON__ || __X86__
    // 普通实现 或者 处理为尾部剩余数据
    for(; i < size; ++i) {
      result[i] = a[i] + b[i];
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "耗时" << duration.count() << "微秒\n";
  }
};

// 特殊类型处理
// 通用模版 - 简单内存比较
template <typename T>
class DataComparator {
public:
  static bool areEqual(const T &a, const T &b) {
    std::cout << "通用版本(内存比较):";
    return a == b;
  }

  static size_t calculateHash(const T &data) {
    std::cout << "通用版本(简单哈希)";
    return std::hash<T>{}(data);
  }
};

// 为C风格字符串特化
template <>
class DataComparator<const char*> {
public:
    static bool areEqual(const char* a, const char* b) {
        std::cout << "const char*特化版本(strcmp): ";
        if (a == b) return true;
        if (!a || !b) return false;
        return std::strcmp(a, b) == 0;
    }

    static size_t calculateHash(const char* data) {
        std::cout << "const char*特化版本(字符串哈希): ";
        if (!data) return 0;

        // 为C字符串提供特殊的哈希算法
        size_t hash = 5381;
        int c;
        while ((c = *data++)) {
            hash = ((hash << 5) + hash) + c;  // hash * 33 + c
        }
        return hash;
    }
};

// 为智能指针特化
template <typename T>
class DataComparator<std::shared_ptr<T>> {
public:
    static bool areEqual(const std::shared_ptr<T>& a, const std::shared_ptr<T>& b) {
        std::cout << "shared_ptr特化版本(内容比较): ";
        if (!a && !b) return true;
        if (!a || !b) return false;
        return *a == *b;  // 比较指向的对象内容
    }

    static size_t calculateHash(const std::shared_ptr<T>& ptr) {
        std::cout << "shared_ptr特化版本(对象哈希): ";
        if (!ptr) return 0;
        return std::hash<T>{}(*ptr);
    }
};

// 为vector<bool>特化（需要特殊处理，因为vector<bool>是特化的）
template <>
class DataComparator<std::vector<bool>> {
public:
    static bool areEqual(const std::vector<bool>& a, const std::vector<bool>& b) {
        std::cout << "vector<bool>特化版本(位级比较): ";
        if (a.size() != b.size()) return false;

        for (size_t i = 0; i < a.size(); ++i) {
            if (a[i] != b[i]) return false;
        }
        return true;
    }
};

void testSpecialHandling() {
    std::cout << "\n=== 特殊类型处理示例 ===" << std::endl;

    // 测试C字符串特化
    const char* str1 = "hello";
    const char* str2 = "hello";
    const char* str3 = "world";

    std::cout << "字符串比较: " << std::boolalpha
              << DataComparator<const char*>::areEqual(str1, str2) << std::endl;
    std::cout << "字符串哈希: "
              << DataComparator<const char*>::calculateHash(str1) << std::endl;

    // 测试智能指针特化
    auto ptr1 = std::make_shared<int>(42);
    auto ptr2 = std::make_shared<int>(42);
    auto ptr3 = std::make_shared<int>(100);

    std::cout << "智能指针比较: "
              << DataComparator<std::shared_ptr<int>>::areEqual(ptr1, ptr2) << std::endl;

    // 测试vector<bool>特化
    std::vector<bool> vec1 = {true, false, true};
    std::vector<bool> vec2 = {true, false, true};

    std::cout << "vector<bool>比较: "
              << DataComparator<std::vector<bool>>::areEqual(vec1, vec2) << std::endl;
}


void testPerformance() {
    const int SIZE = 1000000;

    // 测试float数组
    float* a_float = new float[SIZE];
    float* b_float = new float[SIZE];
    float* result_float = new float[SIZE];

    // 测试int32_t数组
    int32_t* a_int = new int32_t[SIZE];
    int32_t* b_int = new int32_t[SIZE];
    int32_t* result_int = new int32_t[SIZE];

    // 初始化数据
    for (int i = 0; i < SIZE; ++i) {
        a_float[i] = static_cast<float>(i) * 0.1f;
        b_float[i] = static_cast<float>(SIZE - i) * 0.1f;
        a_int[i] = i;
        b_int[i] = SIZE - i;
    }

    std::cout << "=== ARM NEON 性能优化示例 ===" << std::endl;
    std::cout << "数组大小: " << SIZE << " 个元素" << std::endl;

#ifdef __ARM_NEON
    std::cout << "NEON 优化: 可用" << std::endl;
#else
    std::cout << "NEON 优化: 不可用" << std::endl;
#endif

    // 测试float性能
    std::cout << "\n--- float类型测试 ---" << std::endl;
    VectorProcessor<float>::addArrays(a_float, b_float, result_float, SIZE);

    // 测试int32_t性能
    std::cout << "\n--- int32_t类型测试 ---" << std::endl;
    VectorProcessor<int32_t>::addArrays(a_int, b_int, result_int, SIZE);

    // 验证结果正确性
    std::cout << "\n--- 结果验证 ---" << std::endl;
    std::cout << "float结果验证: " << result_float[0] << ", " << result_float[SIZE-1] << std::endl;
    std::cout << "int32_t结果验证: " << result_int[0] << ", " << result_int[SIZE-1] << std::endl;

    // 清理内存
    delete[] a_float;
    delete[] b_float;
    delete[] result_float;
    delete[] a_int;
    delete[] b_int;
    delete[] result_int;
}

int main() {
    testPerformance();
    testSpecialHandling();
    return 0;
}


