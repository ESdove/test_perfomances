# Ctypes vs Subprocess 性能对比测试

## 1. 项目方案

本项目旨在评估 Python 调用 C 语言代码的三种不同方式的性能差异：

1.  **Ctypes 调用 DLL**: 将 C 代码编译为动态链接库 (`.dll`), 使用 Python 的 `ctypes` 模块直接在内存中加载并调用函数。
2.  **Subprocess 调用 EXE**: 将 C 代码编译为可执行文件 (`.exe`), 使用 Python 的 `subprocess` 模块创建新进程执行。
3.  **Subprocess 调用 EXE + 文件读取**: 在方式 2 的基础上，增加从文件读取 C 程序输出结果的步骤，模拟更真实的进程间通信 (IPC) 场景。

**核心逻辑**: C 函数实现两个随机数相加，打印结果，并写入 `gui.txt` 文件。测试脚本对每种方式循环调用 100 次，统计总耗时。

## 2. 运行方式

### 环境要求
- Windows (推荐 MSYS2/MinGW 环境)
- CMake 3.10+
- Python 3.x (需安装 `matplotlib`)

### 编译与运行步骤

1.  **编译 C 代码**
    进入 `performance_test` 目录并使用 CMake 编译：
    ```bash
    cd performance_test
    mkdir build
    cd build
    cmake .. 
    cmake --build . 
    ```
    *注：`CMakeLists.txt` 已配置为静态编译，生成文件位于 `performance_test/output` 目录。*

2.  **运行测试脚本**
    回到 `performance_test` 目录运行 Python 脚本：
    ```bash
    cd ..
    python benchmark.py
    ```

## 3. 测试结果

在 Windows 环境下进行 100 次循环调用的典型测试数据如下（单位：秒）：

| 测试方案 | time (Wall) | perf_counter | process_time (CPU) | 性能评价 |
| :--- | :--- | :--- | :--- | :--- |
| **Ctypes (DLL)** | ~0.21s | ~0.21s | ~0.19s | 🚀 **极快**。包含 DLL 加载和 100 次调用。 |
| **Subprocess (EXE)** | ~3.80s | ~3.80s | ~1.27s | 🐢 **较慢**。进程创建和销毁开销显著。 |
| **Subprocess + Read** | ~4.51s | ~4.51s | ~1.75s | 🐢 **最慢**。在进程开销基础上增加了文件 I/O 操作。 |

*注：Subprocess 方式的 `process_time` 主要消耗在操作系统创建和管理子进程的系统调用上，而 `time` 还包含了等待子进程执行完成的时间。*

## 4. 结果可视化

下图直观展示了三种方式在不同时间度量标准下的性能对比（柱状图越低越好）：

![Benchmark Result](./benchmark_result.png)

### 时间度量说明
*   **time**: 系统墙上时钟时间 (Wall-clock time)，包含所有等待和睡眠时间。
*   **perf_counter**: 高精度性能计数器，测量包含睡眠时间的流逝时间，适合测量短持续时间。
*   **process_time**: 进程CPU时间，不包含睡眠时间 (sleep)。**注意**: 对于 `subprocess` 方式，主进程大部分时间在等待子进程结束（sleep），因此其 `process_time` 可能非常小，这并不代表子进程执行得快，而是代表主进程 CPU 占用低。真实耗时应参考 `time` 或 `perf_counter`。
