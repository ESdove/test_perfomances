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
    cmake .. -G "MinGW Makefiles" 
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

在 Windows 环境下进行 100 次循环调用的典型测试数据如下：

| 测试方案 | 总耗时 (100次) | 平均单次耗时 | 性能评价 |
| :--- | :--- | :--- | :--- |
| **Ctypes (DLL)** | **~0.04s** | ~0.4ms | 🚀 **极快**。直接内存调用，无进程创建开销。 |
| **Subprocess (EXE)** | **~0.82s** | ~8.2ms | 🐢 **较慢**。进程创建和销毁开销显著 (约慢 20 倍)。 |
| **Subprocess + Read** | **~0.61s** | ~6.1ms | 🐢 **较慢**。受系统缓存影响，与纯 Subprocess 差异不大，但理论开销更高。 |

*注：Subprocess 的耗时主要来源于 Windows 昂贵的进程创建（Process Creation）开销。*

## 4. 结果可视化

下图直观展示了三种方式的性能对比（柱状图越低越好）：

![Benchmark Result](performance_test/benchmark_result.png)
