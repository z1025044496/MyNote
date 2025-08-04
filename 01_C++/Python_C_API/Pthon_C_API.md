# python/c api

## 1.Python api调用

### 1.1 c++ 调用python函数(无参)

script/test1.py:
```python
def say:
    print("MMP")
```

main.cpp:
```cpp
int main(int argc, char* argv[])
{
    // （1）初始化 python 解释器
    Py_Initialize();

    // （2）执行 python 语句：
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(../script)");

    // （3）导入 .py 文件：
    Pyobject* module = PyImport_ImportModule("test1");

    if (module == nullptr)
    {
        std::cout << "can not find test1.py" << std:::endl;
        return 1;
    }

    // （4）获取 .py 文件中的函数或类
    PyObject* func = PyObject_GetAttrString(module, "say");

    if (func == nullptr || !PyCallable_Check(func))
    {
        std::cout << "can not find function say()" << std:::endl;
        return 1;
    }

    // (6) 调用 Python 函数
    PyObject_CallObject(func, nullptr);

    // （5）结束 Python 解释器
    Py_Finalize();
    return 0
}
```

### 1.2 c++ 调用python函数(有参)

script/test2.py:
```python
def add(a, b):
    return a + b
```

main.cpp:
```cpp
int main(int argc, char* argv[])
{
    // （1）初始化 python 解释器
    Py_Initialize();

    // （2）执行 python 语句：
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(../script)");

    // （3）导入 .py 文件：
    PyObject* module = PyImport_ImportModule("test2");

    if (module == nullptr)
    {
        std::cout << "can not find test2.py" << std::endl;
        return 1;
    }

    // （4）获取 .py 文件中的函数或类
    PyObject* func = PyObject_GetAttrString(module, "add");

    if (func == nullptr || !PyCallable_Check(func))
    {
        std::cout << "can not find function add()" << std::endl;
        return 1;
    }

    // (5) 设置函数参数
    // 第一种方式
    // PyObject* args = PyTuple_Pack(2, PyLong_FromLong(1), PyLong_FromLong(2));

    // 第二种方式
    PyObject* args = PyTuple_New(2);
    PyTuple_SetItem(args, 0, Py_BuildValue("i", 1));
    PyTuple_SetItem(args, 1, Py_BuildValue("i", 2));

    // (6) 调用 Python 函数并接受返回值
    PyObject* result = PyObject_CallObject(func, args);

    if (result != nullptr)
    {
        int sum = 0;
        PyArg_Parse(result, "i", &sum);
        std::cout << "1 + 2 = " << sum << std::endl;
    }

    // （7）释放资源（没有其他操作的情况下会自动释放）
    Py_DECREF(args);
    Py_DECREF(func);
    Py_DECREF(module);

    // （8）结束 Python 解释器
    Py_Finalize();
    return 0;
}
```

### 1.3 c++调用python类

script/test3.py:
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print("Hello, " + self.name + ". You are " + str(self.age) + " years old.")
        return True
```

main.cpp:
```cpp
int main(int argc, char* argv[])
{
    // （1）初始化 python 解释器
    Py_Initialize();

    // （2）执行 python 语句：
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append(../script)");

    // （3）导入 .py 文件：
    PyObject* module = PyImport_ImportModule("test3");

    if (module == nullptr)
    {
        std::cout << "can not find test3.py" << std::endl;
        return 1;
    }

    // （4）获取 .py 文件中的类
    PyObject* cls = PyObject_GetAttrString(module, "Person");

    if (cls == nullptr)
    {
        std::cout << "can not find class Person" << std::endl;
        return 1;
    }

    // （5）给类的构造函数传递参数
    PyObject* args = PyTuple_New(2);
    PyTuple_SetItem(args, 0, Py_BuildValue("s", "potter"));
    PyTuple_SetItem(args, 1, Py_BuildValue("i", 10));

    // （6）创建类的实例
    PyObject* instance = PyObject_CallObject(cls, args);

    if (instance == nullptr)
    {
        std::cout << "can not create instance of Person" << std::endl;
        return 1;
    }

    // （7）调用实例方法
    PyObject* method = PyObject_GetAttrString(instance, "say_hello");

    if (method == nullptr || !PyCallable_Check(method))
    {
        std::cout << "can not find method say_hello()" << std::endl;
        return 1;
    }

    PyObject_CallObject(method, nullptr);

    // （7）释放资源（没有其他操作的情况下会自动释放）
    Py_DECREF(method);
    Py_DECREF(instance);
    Py_DECREF(cls);
    Py_DECREF(module);

    // （8）结束 Python 解释器
    Py_Finalize();
    return 0;
}
```

## 2.引用计数

> Py_ssize_t Py_REFCNT(PyObject *o)

获取`Python`对象`o`的引用计数。

> void Py_SET_REFCNT(PyObject *o, Py_ssize_t refcnt)

将对象`o`的引用计数器设为`refcnt`。

> void Py_INCREF(PyObject *o)

对象`o`不能为`NULL`

表示为对象`o`获取一个新的`strong reference`，指明该对象正在被使用且不应被销毁。

当对象使用完毕后，可调用`Py_DECREF()`释放它。

> void Py_XINCREF(PyObject *o)

功能与`Py_INCREF`功能相同，只是对象`o`可以是`NULL`

> PyObject *Py_NewRef(PyObject *o)

对象`o`不能为`NULL`

为对象创建一个新的`strong reference:`在`o`上调用`Py_INCREF()`并返回对象`o`。

当不再需要这个`strong reference`时，应当在其上调用`Py_DECREF()`来释放引用。

> PyObject *Py_XNewRef(PyObject *o)

功能与`Py_NewRef`功能相同，只是对象`o`可以是`NULL`

> void Py_DECREF(PyObject *o)

对象`o`不能为`NULL`

释放一个指向对象`o`的`strong reference`，表明该引用不再被使用。

当最后一个`strong reference`被释放时(即对象的引用计数变为0)，将会唤起该对象所属类型的`deallocation`函数(它必须不为`NULL`)。

> void Py_XDECREF(PyObject *o)

功能与`Py_DECREF`功能相同，只是对象`o`可以是`NULL`

> void Py_CLEAR(PyObject *o)

功能与`Py_DECREF`功能相同，只是对象`o`可以是`NULL`

当传入`NULL`时，因为该宏使用一个临时变量并在释放引用之前将参数设为`NULL`。

> void Py_IncRef(PyObject *o)

`Py_XINCREF()`的函数版本

> void Py_DecRef(PyObject *o)

`Py_XDECREF()`的函数版本

> Py_SETREF(dst, src)

安全地释放一个指向对象`dst`的`strong reference`，并将`dst`设为`src`。

> Py_XSETREF(dst, src)

使用`Py_XDECREF()`代替`Py_DECREF()`的`Py_SETREF`宏的变种。
