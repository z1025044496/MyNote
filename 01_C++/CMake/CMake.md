# 1. CMake概述

CMake 是一个项目构建工具，并且是跨平台的。关于项目构建我们所熟知的还有Makefile（通过 make 命令进行项目的构建），大多是IDE软件都集成了make，比如：VS 的 nmake、linux 下的 GNU make、Qt 的 qmake等，如果自己动手写 makefile，会发现，makefile 通常依赖于当前的编译平台，而且编写 makefile 的工作量比较大，解决依赖关系时也容易出错。

而 CMake 恰好能解决上述问题， 其允许开发者指定整个工程的编译流程，在根据编译平台，**自动生成本地化的Makefile和工程文件**，最后用户只需`make`编译即可，所以可以把CMake看成一款自动生成 Makefile的工具，其编译流程如下图：

![](../../image/cmake编译流程.png)

* 蓝色虚线表示使用`makefile`构建项目的过程
* 红色实线表示使用`cmake`构建项目的过程

> [!TIP]
> **优点**
> 1. 跨平台
> 2. 能够管理大型项目
> 3. 简化编译构建过程和编译过程
> 4. 可扩展：可以为 cmake 编写特定功能的模块，扩充 cmake 功能

# 2. CMake使用

`CMake`支持大写、小写、混合大小写的命令。如果在编写CMakeLists.txt文件时使用的工具有对应的命令提示，那么大小写随缘即可，不要太过在意。

## 2.1 注释

### 2.1.1 注释行

`CMake`使用`#`进行行注释，可以放在任何位置。

```php
# 这是一个 CMakeLists.txt 文件
cmake_minimum_required(VERSION 3.0.0)
```

### 2.1.2 块注释

`CMake`使用`#[[ ]]`形式进行块注释。

```php
#[[ 这是一个 CMakeLists.txt 文件。
这是一个 CMakeLists.txt 文件
这是一个 CMakeLists.txt 文件]]
cmake_minimum_required(VERSION 3.0.0)
```

## 2.2 只有源文件

### 2.2.1 共处一室

1. 准备一下几个文件
 
* add.cpp

```cpp
#include <stdio.h>
#include "head.h"

int add(int a, int b)
{
    return a+b;
}
```

* sub.cpp

```cpp
#include <stdio.h>
#include "head.h"

int sub(int a, int b)
{
    return a - b;
}
```

* mult.cpp

```cpp
#include <stdio.h>
#include "head.h"

int mult(int a, int b)
{
    return a * b;
}
```

* div.cpp

```cpp
#include <stdio.h>
#include "head.h"

double div(int a, int b)
{
    return (double)a / b;
}
```

* head.h

```cpp
#ifndef _HEAD_H_
#define _HEAD_H_

int add(int a, int b);
int sub(int a, int b);
int mult(int a, int b);
float div(int a, int b);

#endif
```

* main.cpp

```cpp
#include <stdio.h>
#include "head.h"

int main()
{
    int a = 20;
    int b = 12;

    printf("a = %d, b = %d\n", a, b);
    printf("a + b = %d\n", add(a, b));
    printf("a - b = %d\n", sub(a, b));
    printf("a * b = %d\n", mult(a, b));
    printf("a / b = %f\n", div(a, b));

    return 0;
}
```

2. 上述文件的目录结构如下：
   
```term
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ tree
.
├── add.cpp
├── div.cpp
├── head.h
├── main.cpp
├── mult.cpp
└── sub.cpp
```

3. 生成`CMakeLists.txt`文件

在上述源文件所在目录下添加一个新文件`CMakeLists.txt`，文件内容如下：

```php
cmake_minimum_required(VERSION 3.15)
project(CALC)
add_executable(app add.cpp div.cpp main.cpp mult.cpp sub.cpp)
```
* `cmake_minimum_required`：指定使用的cmake的最低版本
  * 可选，非必须，如果不加可能会有警告

* `project`：定义工程名称，并可指定工程的版本、工程描述、web主页地址、支持的语言（默认情况支持所有语言），如果不需要这些都是可以忽略的，只需要指定出工程名字即可。

    ```php
    # PROJECT 指令的语法是：
    project(<PROJECT-NAME> [<language-name>...])
    project(<PROJECT-NAME>
        [VERSION <major>[.<minor>[.<patch>[.<tweak>]]]]
        [DESCRIPTION <project-description-string>]
        [HOMEPAGE_URL <url-string>]
        [LANGUAGES <language-name>...])
    ```

* `add_executable`：定义工程会生成一个可执行程序

    ```php
    add_executable(可执行程序名 源文件名称)
    ```

  * 这里的可执行程序名和project中的项目名没有任何关系

  * 源文件名可以是一个也可以是多个，如有多个可用空格或;间隔
        ```php
        # 样式1
        add_executable(app add.cpp div.cpp main.cpp mult.cpp sub.cpp)
        # 样式2
        add_executable(app add.cpp;div.cpp;main.cpp;mult.cpp;sub.cpp)
        ```
4. 执行`cmake`命令

```term
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ tree
.
├── CMakeLists.txt
├── add.cpp
├── div.cpp
├── head.h
├── main.cpp
├── mult.cpp
└── sub.cpp

0 directories, 7 files
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ cmake .
-- The C compiler identification is GNU 11.4.0
-- The CXX compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done (1.9s)
-- Generating done (0.1s)
-- Build files have been written to: /mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1
```

当执行`cmake`命令之后，`CMakeLists.txt`中的命令就会被执行，所以一定要注意给`cmake`命令指定路径的时候一定不能出错。

执行命令之后，看一下源文件所在目录中是否多了一些文件：

```term
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ tree -L 1
.
├── CMakeCache.txt
├── CMakeFiles
├── CMakeLists.txt
├── Makefile
├── add.cpp
├── cmake_install.cmake
├── div.cpp
├── head.h
├── main.cpp
├── mult.cpp
└── sub.cpp
```

我们可以看到在对应的目录下生成了一个`makefile`文件，此时再执行`make`命令，就可以对项目进行构建得到所需的可执行程序了。

```term
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ tree -L 1
.
├── CMakeCache.txt
├── CMakeFiles
├── CMakeLists.txt
├── Makefile
├── add.cpp
├── app
├── cmake_install.cmake
├── div.cpp
├── head.h
├── main.cpp
├── mult.cpp
└── sub.cpp
```

最终可执行程序**app**就被编译出来了（这个名字是在**CMakeLists.txt**中指定的）。

```term
zhaohaifei@XTZJ-20221120IX:/mnt/d/MyGithubNote/MyNote/code/CMake-demo/V1$ ./app
a = 20, b = 12
a + b = 32
a - b = 8
a * b = 240
a / b = 1.666667
```

### 2.2.2 VIP包房

## 2.3 私人定制

## 2.4 搜索文件

## 2.5 包含头文件

## 2.6 制作动态库或静态库

## 2.7 日志

## 2.8 变量操作 

# 3. 预宏定义

# 4. 嵌套的CMake

# 5. 流程控制