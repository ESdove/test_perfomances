cmake_minimum_required(VERSION 3.10)
project(PerformanceTest)

# 设置构建输出目录
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/output)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/output)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/output)

# 生成 DLL (定义 BUILD_DLL 宏)
add_library(api SHARED core.c)
target_compile_definitions(api PRIVATE BUILD_DLL)
target_link_options(api PRIVATE "-static")

# 生成 EXE (定义 BUILD_EXE 宏)
add_executable(app core.c)
target_compile_definitions(app PRIVATE BUILD_EXE)
target_link_options(app PRIVATE "-static")
