#include <iostream>
#include <thread>

void Fun01()
{
    std::cout << "this test01 fun!" << std::endl;
}

void test01()
{
    std::thread thA(Fun01);
    thA.join();
}

struct MyStruct
{
    MyStruct()
    {
        std::cout << "this is constructor fun of MyStruct" << std::endl;
    }

    void operator()() const 
    { 
        std::cout << "this is overload() fun of MyStruct" << std::endl; 
    }
};

MyStruct stest(){

}

#include <functional>

void test02()
{
    MyStruct stA;

    std::function< MyStruct() > fcn;

    std::thread t1(stA);
    std::thread t2(MyStruct());
    std::thread t3{MyStruct()};
    std::thread t4((MyStruct()));
    std::thread t5{[] { std::cout << "this is lambda fun" << std::endl; }};

    t1.join();
    t3.join();
    t4.join();
    t5.join();
}

class A {
public:
    A(int& x) : x(x) {}

    void operator()() const 
    {
        for (int i = 0; i < 1000000; ++i) 
        {
            // call(x);  
            // 存在对象析构后引用空悬的隐患
            std::cout << x << std::endl;
        }
    }

private:
    void call(int& x) {}

private:
    int& x;
};

void f() {
    int x = 0;
    A a{x};
    std::thread t{a};
    t.detach();  // 不等待 t 结束
}  // 函数结束后 t 可能还在运行，而 x 已经销毁，a.x_ 为空悬引用

void test03()
{
    std::thread t{f};  // 导致空悬引用
    t.join();
}

int main()
{
    std::cout << "*************start**************" << std::endl;
    test02();
    std::cout << "**************end***************" << std::endl;
}