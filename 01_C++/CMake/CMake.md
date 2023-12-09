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

```cmake
# 这是一个 CMakeLists.txt 文件
cmake_minimum_required(VERSION 3.0.0)
```

### 2.1.2 块注释

`CMake`使用`#[[ ]]`形式进行块注释。

```cmake
#[[ 这是一个 CMakeLists.txt 文件。
这是一个 CMakeLists.txt 文件
这是一个 CMakeLists.txt 文件]]
cmake_minimum_required(VERSION 3.0.0)
```

# 3. 预宏定义

# 4. 嵌套的CMake

# 5. 流程控制