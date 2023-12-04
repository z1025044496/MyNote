# CMake如何构建简单的Target

要我说一种现代 CMake 最核心的特性，当属 Target。现代 CMake 围绕着 Target 这一核心特性组织 C/C++ 项目的结构，管理其配置、编译、单元测试、打包等。

CMake 有三个基本命令，用于定义 CMake Target，它们分别是：

* add_executable()
* add_library()
* add_custom_target()

## add_executable()

``` cmake
add_executable(<name> [WIN32] [MACOSX_BUNDLE]
    [EXCLUDE_FROM_ALL]
    [source1] [source2 ...]
)
```
第一个参数是 Target 的名字，这个参数必须提供。

第二个参数 WIN32 是可选参数，Windows 平台特定的参数，现在你不用管它的意思，不要使用它即可。后续我们需要使用到它的时候会说明其含义。

第三个参数 MACOSX_BUNDLE 同第二个参数，是 Apple 平台的特定参数，先忽略。

第四个参数 EXCLUDE_FROM_ALL 如果存在，那 CMake 默认构建的时候就不会构建这个 Target。

后续可选参数均为构建该可执行文件所需的源码，在这里可以省略，通过其他命令单独指定源码。但是对于入门，我们直接在这里指定源码文件即可。

下面是一个例子
``` cmake
cmake_minimum_required(VERSION 3.26 FATAL_ERROR)

add_executable(main main.cpp)
```

## add_library()

``` cmake
add_library(<name> [STATIC | SHARED | MODULE]
    [EXCLUDE_FROM_ALL]
    [<source>...]
)
```

签名和 add_executable() 非常相似，该命令用于定义构建成库文件的 Target。

这里只讲差异，add_library() 命令支持可选的三个互斥参数：STATIC | SHARED | MODULE。  
> STATIC 静态库  
> SHARED 动态库  
> MODULE 插件库

这三个参数要么都没有，要么只能有一个。对于简单的例子，我们可以指定构建库为 STATIC（静态库）、SHARED（动态库）、MODULE（类似于动态库，不过不会被其他库或者可执行程序链接，用于插件式框架的软件的插件构建）。

当然最佳实践是不要自己在 CMakeLists.txt 中指定这几个参数，而是把主动权交给构建者，通过 `cmake -DBUILD_SHARED_LIBS=YES` 的形式传值告诉其需要构建哪种库。这个现在不用管，忽略即可，后续更深入的课程会详细介绍。

## add_custom_target

## 关于Target链接

## 最佳实践