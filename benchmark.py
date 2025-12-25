import os
import time
import subprocess
import ctypes
import sys
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
        # Load DLL
        lib = ctypes.CDLL(dll_path)
        # 根据 C 代码：int add()
        add_func = lib.add
        add_func.argtypes = []
        add_func.restype = ctypes.c_int
        
        start_time = time.time()
        for _ in range(n):
            res = add_func()
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Ctypes test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

# 2. Subprocess EXE 测试
def test_subprocess(exe_path, n=100):
    print(f"Running Subprocess test ({n} iterations)...")
    try:
        start_time = time.time()
        for _ in range(n):
            # capture_output=True 防止 C 的 printf 刷屏
            subprocess.run([exe_path], capture_output=True) 
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Subprocess test failed: {e}")
        return None

# 3. Subprocess EXE + Read File 测试
def test_subprocess_io(exe_path, n=100):
    print(f"Running Subprocess + IO test ({n} iterations)...")
    try:
        start_time = time.time()
        for _ in range(n):
            subprocess.run([exe_path], capture_output=True)
            if os.path.exists(GUI_TXT):
                with open(GUI_TXT, "r") as f:
                    _ = f.read()
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Subprocess IO test failed: {e}")
        return None

def visualize_results(results):
    if not results:
        print("No results to visualize.")
        return

    labels = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=['#4CAF50', '#2196F3', '#FF9800'])
    
    plt.title('Performance Comparison: Ctypes vs Subprocess')
    plt.xlabel('Method')
    plt.ylabel('Total Time (seconds) for 100 iterations')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 在柱状图上显示数值
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.4f}s', ha='center', va='bottom')

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
    for k, v in results.items():
        print(f"{k}: {v:.4f}s")

    visualize_results(results)

if __name__ == "__main__":
    main()
