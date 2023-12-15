# std::thread

## 传递参数

1. 将参数作为`std::thread`构造函数的附加参数

   > 需要注意的是，这些参数会拷贝至新线程的内存空间中(同临时变量一样)。即使函数中的参数是引用的形式，拷贝操作也会执行。来看一个例子： 

   ```cpp
   void f(int i, std::string const& s);
   std::thread t(f, 3, "hello");
   ``` 
   
   > 注意，函数f需要一个std::string对象作为第二个参数，但这里使用的是字符串的字面值，也就是char const *类型，线程的上下文完成字面值向std::string的转化。需要特别注意，指向动态变量的指针作为参数的情况，代码如下：

   ```c++
   void f(int i,std::string const& s);
   void oops(int some_param)
   {
    char buffer[1024]; // 1
    sprintf(buffer, "%i",some_param);
    std::thread t(f,3,buffer); // 2
    t.detach();
   }
   ```

   > buffer①是一个指针变量，指向局部变量，然后此局部变量通过buffer传递到新线程中②。此时，函数oops可能会在buffer转换成std::string之前结束，从而导致未定义的行为。因为，无法保证隐式转换的操作和std::thread构造函数的拷贝操作的顺序，有可能std::thread的构造函数拷贝的是转换前的变量(buffer指针)。解决方案就是在传递到std::thread构造函数之前，就将字面值转化为std::string：

   ```cpp
   void f(int i,std::string const& s);
   void not_oops(int some_param)
   {
    char buffer[1024];
    sprintf(buffer,"%i",some_param);
    std::thread t(f,3,std::string(buffer));  // 使用std::string，避免悬空指针
    t.detach();
   }
   ```

   > 相反的情形(期望传递一个非常量引用，但复制了整个对象)倒是不会出现，因为会出现编译错误。比如，尝试使用线程更新引用传递的数据结构：

   ```cpp
   void update_data_for_widget(widget_id w,widget_data& data); // 1
   void oops_again(widget_id w)
   {
      widget_data data;
      std::thread t(update_data_for_widget,w,data); // 2
      display_status();
      t.join();
      process_widget_data(data);
   }
   ```

   > 虽然update_data_for_widget①的第二个参数期待传入一个引用，但std::thread的构造函数②并不知晓，构造函数无视函数参数类型，盲目地拷贝已提供的变量。不过，内部代码会将拷贝的参数以右值的方式进行传递，这是为了那些只支持移动的类型，而后会尝试以右值为实参调用update_data_for_widget。但因为函数期望的是一个非常量引用作为参数(而非右值)，所以会在编译时出错。对于熟悉std::bind的开发者来说，问题的解决办法很简单：可以使用std::ref将参数转换成引用的形式。因此可将线程的调用改为以下形式：

   ```cpp 
   std::thread t(update_data_for_widget,w,std::ref(data));
   ```

2. 传递一个成员函数指针作为线程函数，并提供一个合适的对象指针作为第一个参数
   ```cpp
   class X
   {
    public:
    void do_lengthy_work();
   };
   X my_x;
   std::thread t(&X::do_lengthy_work, &my_x); // 1
   ```

   ```cpp
   class X
   {
    public:
    void do_lengthy_work(int);
   };
   X my_x;
   int num(0);
   std::thread t(&X::do_lengthy_work, &my_x, num);
   ```

3. 移动构造
   
   ```cpp
   void process_big_object(std::unique_ptr<big_object>);

   std::unique_ptr<big_object> p(new big_object);
   p->prepare_data(42);
   std::thread t(process_big_object,std::move(p));
   ```

   > 通过在std::thread构造函数中执行std::move(p)，big_object 对象的所有权首先被转移到新创建线程的的内部存储中，之后再传递给process_big_object函数。

   C++标准线程库中和std::unique_ptr在所属权上相似的类有好几种，std::thread为其中之一。虽然，std::thread不像std::unique_ptr能占有动态对象的所有权，但是它能占有其他资源：每个实例都负责管理一个线程。线程的所有权可以在多个std::thread实例中转移，这依赖于std::thread实例的**可移动**且**不可复制性**。不可复制性表示在某一时间点，一个std::thread实例只能关联一个执行线程。可移动性使得开发者可以自己决定，哪个实例拥有线程实际执行的所有权。

## 转移线程所有权

假设通过新线程返回的所有权去调用一个需要后台启动线程的函数，并需要在函数中转移线程的所有权。这些操作都要等待线程结束才能进行，并且需要线程的所有权能够进行转移。

这就是将移动操作引入`std::thread`的原因，C++标准库中有很多资源占有(resource-owning)类型，比如`std::ifstream`，`std::unique_ptr`还有`std::thread`都是**可移动，但不可复制**。这说明执行线程的所有权可以在`std::thread`实例中移动，下面将展示一个例子。例子中，创建了两个执行线程，并在`std::thread`实例之间(t1，t2和t3)转移所有权：   

```cpp
void some_function();
void some_other_function();
std::thread t1(some_function);           // 1
std::thread t2=std::move(t1);            // 2
t1=std::thread(some_other_function);     // 3
std::thread t3;                          // 4
t3=std::move(t2);                        // 5
t1=std::move(t3);                        // 6 赋值操作将使程序崩溃
```

首先，新线程与t1相关联①。当显式使用std::move()创建t2后②，t1的所有权就转移给了t2。之后，t1和执行线程已经没有关联了，执行some_function的函数线程与t2关联。

然后，临时std::thread对象相关的线程启动了③。为什么不显式调用std::move()转移所有权呢？因为，所有者是一个临时对象——移动操作将会隐式的调用。

t3使用默认构造方式创建④，没有与任何线程进行关联。调用std::move()将t2关联线程的所有权转移到t3中⑤。因为t2是一个命名对象，需要显式的调用std::move()。移动操作⑤完成后，t1与执行some_other_function的线程相关联，t2与任何线程都无关联，t3与执行some_function的线程相关联。

最后一个移动操作，将some_function线程的所有权转移⑥给t1。不过，t1已经有了一个关联的线程(执行some_other_function的线程)，所以这里系统直接调用`std::terminate()`终止程序继续运行。这样做(不抛出异常，`std::terminate()`是noexcept函数)是为了保证与`std::thread`的析构函数的行为一致。2.1.1节中，需要在线程对象析构前，显式的等待线程完成，或者分离它，进行赋值时也需要满足这些条件(说明：不能通过赋新值给`std::thread`对象的方式来"丢弃"一个线程)。