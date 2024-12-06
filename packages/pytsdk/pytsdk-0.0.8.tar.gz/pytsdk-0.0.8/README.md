# 大疆红外测温SDK调用封装

为提供给python调用， 尝试将大疆红外测温sdk， 通过`pybind11`封装为python模块。 而在实际封装过程中存在`内存泄漏`， 于是放弃。 直接利用python的`ctypes`调用dll, 反而不存在内存泄漏。


> 大疆红外测温sdk下载地址为[https://www.dji.com/cn/downloads/softwares/dji-thermal-sdk](https://www.dji.com/cn/downloads/softwares/dji-thermal-sdk)


## 如何切换
在thermal/CMakeLists.txt中存在COMPILE_TO_DLL选项用于切换pybind11方式还是dll方式。


## 测试与检测内存泄漏

Windows检测内存泄漏参考[使用 CRT 库查找内存泄漏](https://learn.microsoft.com/zh-cn/cpp/c-runtime-library/find-memory-leaks-using-the-crt-library?view=msvc-170)。 具体在代码中使用：

在合适的地方包含如下代码：
```c++
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
```

建议在程序开始处编写如下代码:
```c++
_CrtDumpMemoryLeaks();
_CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
_CrtSetReportMode(_CRT_WARN, _CRTDBG_MODE_DEBUG);
```

运行后即可在命令行窗口观察到内存泄漏报告


如何测试内存泄漏？通过python的`psutil`很方便对程序的内存情况进行监控， 案例如下:
```python
import psutil
import os

process = psutil.Process(os.getpid())

print(f"RSS memory: {process.memory_info().rss / (1024 * 1024):.2f} MB")

# 此处为检测核心代码， 内存消耗的代码

print(f"RSS memory: {process.memory_info().rss / (1024 * 1024):.2f} MB")
```

> RSS是指Resident Set Size 实际使用物理内存


## 示例
```python

thermal = ThermalInfo(True)
thermal.open(r"0B2D25BC332B40D09D8E6DD60050B00A.jpg")
temperature = thermal.get_temperature()
raw_image = thermal.get_raw_image()
thermal.close()

```











