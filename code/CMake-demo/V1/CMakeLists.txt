cmake_minimum_required(VERSION 3.15)

project(CALC)

# set(SRC_LIST add.cpp div.cpp main.cpp mult.cpp sub.cpp)
# aux_source_directory(${PROJECT_SOURCE_DIR} SRC_LIST)
file(GLOB SRC_LIST ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)

set(EXECUTABLE_OUTPUT_PATH ../bin)

set(CMAKE_CXX_STANDARD 11)

add_executable(app ${SRC_LIST})