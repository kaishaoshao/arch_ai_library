#include <iostream>
using namespace std;

#define __STL_TEMPLATE_NULL
template <class Key>
struct hashes
{
  void operator()() {
    cout << "hasher<T>" <<endl;
  }
};

// explicit
// 关键字用于防止编译器进行隐式类型转换或复制初始化，只允许显式调用构造函数。
// template <class Key>
// explicit // specialization
// __STL_TEMPLATE_NULL struct hashes<char>
// {
//   void operator()() {
//     cout << "hashes<char>" << endl;
//   }
// };
// __STL_TEMPLATE_NULL struct hashes<unsigned char>
// {
//   void operator()() {
//     cout << "hashes<char>" <<endl;
//   }
// };


int main()
{
  hashes<long> t1;
  hashes<char> t2;
  hashes<unsigned char> t3;

  t1();
  t2();
  t3();
  return 0;
}
