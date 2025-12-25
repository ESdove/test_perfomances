#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifdef _WIN32
  #define EXPORT __declspec(dllexport)
#else
  #define EXPORT
#endif

// 核心逻辑函数：生成随机数，相加，打印，写入文件，返回结果
int core_add() {
    int a = rand() % 1000;
    int b = rand() % 1000;
    int result = a + b;

    // 1. Print result (输出到标准输出)
    printf("Result: %d\n", result);
    
    // 2. Write to gui.txt (写入文件)
    FILE *fp = fopen("gui.txt", "w");
    if (fp) {
        fprintf(fp, "%d", result);
        fclose(fp);
    }

    // 3. Return result
    return result;
}

#ifdef BUILD_DLL
// DLL 导出函数
EXPORT int add() {
    // 这里的随机数种子通常由宿主程序控制，或者每次调用都初始化（不推荐，因为如果调用很快，时间戳相同）
    // 为了简单模拟，我们这里只负责调用核心逻辑
    return core_add();
}
#endif

#ifdef BUILD_EXE
int main() {
    // EXE 运行时初始化随机数种子
    srand((unsigned int)time(NULL));
    // 返回值作为进程退出码
    return core_add();
}
#endif
