import os
import time
import subprocess
import ctypes
import matplotlib.pyplot as plt

# 配置路径 - 直接指向 output 目录
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 用户指定的文件名
DLL_NAME = "msys-api.dll" 
EXE_NAME = "app.exe"
GUI_TXT = "gui.txt"

def get_binary_path(name):
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        print(f"Error: File not found at {path}")
        return None
    return path

# 1. Ctypes 测试
def test_ctypes(dll_path, n=100):
    print(f"Running Ctypes test ({n} iterations)...")
    try:
        t_time_start = time.time()
        t_perf_start = time.perf_counter()
        t_proc_start = time.process_time()

        # Load DLL
        lib = ctypes.CDLL(dll_path)
        # 根据 C 代码：int add()
        add_func = lib.add
        add_func.argtypes = []
        add_func.restype = ctypes.c_int
        
        for _ in range(n):
            res = add_func()

        t_time_end = time.time()
        t_perf_end = time.perf_counter()
        t_proc_end = time.process_time()
        
        return {
            "time": t_time_end - t_time_start,
            "perf_counter": t_perf_end - t_perf_start,
            "process_time": t_proc_end - t_proc_start
        }
    except Exception as e:
        print(f"Ctypes test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# 2. Subprocess EXE 测试
def test_subprocess(exe_path, n=100):
    print(f"Running Subprocess test ({n} iterations)...")
    try:
        t_time_start = time.time()
        t_perf_start = time.perf_counter()
        t_proc_start = time.process_time()

        for _ in range(n):
            # capture_output=True 防止 C 的 printf 刷屏
            subprocess.run([exe_path], capture_output=True) 

        t_time_end = time.time()
        t_perf_end = time.perf_counter()
        t_proc_end = time.process_time()

        return {
            "time": t_time_end - t_time_start,
            "perf_counter": t_perf_end - t_perf_start,
            "process_time": t_proc_end - t_proc_start
        }
    except Exception as e:
        print(f"Subprocess test failed: {e}")
        return None

# 3. Subprocess EXE + Read File 测试
def test_subprocess_io(exe_path, n=100):
    print(f"Running Subprocess + IO test ({n} iterations)...")
    try:
        t_time_start = time.time()
        t_perf_start = time.perf_counter()
        t_proc_start = time.process_time()

        for _ in range(n):
            # 删除 gui.txt, 避免文件缓存影响
            if os.path.exists(GUI_TXT):
                try:
                    os.remove(GUI_TXT)
                except OSError:
                    pass

            subprocess.run([exe_path], capture_output=True)
            if os.path.exists(GUI_TXT):
                with open(GUI_TXT, "r") as f:
                    _ = f.read()

        t_time_end = time.time()
        t_perf_end = time.perf_counter()
        t_proc_end = time.process_time()

        return {
            "time": t_time_end - t_time_start,
            "perf_counter": t_perf_end - t_perf_start,
            "process_time": t_proc_end - t_proc_start
        }
    except Exception as e:
        print(f"Subprocess IO test failed: {e}")
        return None

import numpy as np

def visualize_results(results):
    if not results:
        print("No results to visualize.")
        return

    # 准备数据
    methods = list(results.keys())  # ['Ctypes', 'Subprocess', 'Subprocess + Read']
    metrics = ['time', 'perf_counter', 'process_time']
    
    # 颜色映射
    colors = ['#4CAF50', '#2196F3', '#FF9800'] # 对应三种指标
    
    fig, ax = plt.subplots(figsize=(12, 8))

    x = np.arange(len(methods))  # 方法标签位置
    width = 0.25  # 柱子宽度

    # 绘制每个指标的柱子
    # time: x - width
    # perf_counter: x
    # process_time: x + width

    rects1 = ax.bar(x - width, [results[m]['time'] for m in methods], width, label='time', color=colors[0])
    rects2 = ax.bar(x, [results[m]['perf_counter'] for m in methods], width, label='perf_counter', color=colors[1])
    rects3 = ax.bar(x + width, [results[m]['process_time'] for m in methods], width, label='process_time', color=colors[2])

    # 添加文本标签
    ax.set_ylabel('Total Time (s)')
    ax.set_title('Performance Comparison by Method and Metric')
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    def autolabel(rects):
        """在每个柱子上方显示数值"""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.savefig('benchmark_result.png')
    print("Chart saved to benchmark_result.png")


def main():
    print(f"Searching binaries in: {OUTPUT_DIR}")
    dll_path = get_binary_path(DLL_NAME)
    exe_path = get_binary_path(EXE_NAME)

    if not dll_path or not exe_path:
        print("Aborting: Binaries not found.")
        return

    print(f"Found DLL: {dll_path}")
    print(f"Found EXE: {exe_path}")

    # 清理旧的 txt
    if os.path.exists(GUI_TXT):
        try:
            os.remove(GUI_TXT)
        except Exception:
            pass

    # 真实测试
    n = 100
    results = {}
    
    t1 = test_ctypes(dll_path, n)
    if t1 is not None: results['Ctypes'] = t1

    t2 = test_subprocess(exe_path, n)
    if t2 is not None: results['Subprocess'] = t2

    t3 = test_subprocess_io(exe_path, n)
    if t3 is not None: results['Subprocess + Read'] = t3

    print("\n--- Final Results ---")
    summary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.txt")
    print(f"Writing results to {summary_path}")
    try:
        with open(summary_path, "w") as f_summary:
            f_summary.write("--- Final Results ---\n")
            for method, metrics in results.items():
                print(f"{method}:")
                f_summary.write(f"{method}:\n")
                print(f"  time:         {metrics['time']:.4f}s")
                f_summary.write(f"  time:         {metrics['time']:.4f}s\n")
                print(f"  perf_counter: {metrics['perf_counter']:.4f}s")
                f_summary.write(f"  perf_counter: {metrics['perf_counter']:.4f}s\n")
                print(f"  process_time: {metrics['process_time']:.4f}s")
                f_summary.write(f"  process_time: {metrics['process_time']:.4f}s\n")
    except Exception as e:
        print(f"Failed to write summary: {e}")

    visualize_results(results)

if __name__ == "__main__":
    main()
