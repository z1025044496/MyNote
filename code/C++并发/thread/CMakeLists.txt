cmake_minimum_required(VERSION 3.15)

project(THREAD_TEST)

set(CMAKE_CXX_STANDARD 11)

set(SRC_LIST 
    test01_thread.cpp)

add_executable(${PROJECT_NAME} ${SRC_LIST})

target_link_libraries (${PROJECT_NAME} pthread) 