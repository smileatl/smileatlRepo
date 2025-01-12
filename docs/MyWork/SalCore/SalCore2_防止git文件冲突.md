## 1、这么做的，但是出现了e.finfo访问不了的问题，是因为没有初始化吗

### **问题所在：**

```cpp
struct Entry
{
    enum Type { FILE, DIRECTORY, LINK };

    Type type;
    std::string path;
    #ifndef PF_PLATFORM_LINUX
    apr_finfo_t* finfo;
    #endif
};

class Iterator
{
    public:

    Iterator(const Path & path);
    Iterator(const std::string & path);
    ~Iterator();

    // Resets directory to start. Subsequent call to next() 
    // will retrieve the first entry
    void reset();
    // get next directory entry
    Entry * next(Entry & e);
    private:
    Iterator();
    Iterator(const Iterator &);

    void init(const std::string & path);
    private:
    std::string path_;
    #ifdef PF_PLATFORM_LINUX
    DIR * handle_;
    #else
    apr_dir_t * handle_;
    apr_pool_t * pool_;
    #endif
};

Entry * Iterator::next(Entry & e)
{
    apr_int32_t wanted = APR_FINFO_LINK | APR_FINFO_NAME | APR_FINFO_TYPE;
    apr_status_t res = ::apr_dir_read(e.finfo, wanted, handle_);

    // No more entries
    if (APR_STATUS_IS_ENOENT(res))
        return NULL;

    if (res != 0)
    {
        CHECK(res == APR_INCOMPLETE) 
            << "Couldn't read next dir entry." 
            << " Error code: " << APR_TO_OS_ERROR(res);
        CHECK(((e.finfo->valid & wanted) | APR_FINFO_LINK) == wanted) 
            << "Couldn't retrieve all fields. Valid mask=" << e.finfo->valid; 
    } 


    e.type = (e.finfo->filetype == APR_DIR) ? Directory::Entry::DIRECTORY 
        : Directory::Entry::FILE;
    e.path = e.finfo->name;                               

    // Skip '.' and '..' directories
    if (e.type == Directory::Entry::DIRECTORY && 
        (e.finfo->name == std::string(".") || e.finfo->name == std::string("..")))
        return next(e);
    else
        return &e;
}
```

### 解决办法

是的，出现`e.finfo`访问不了的问题很可能是因为没有正确初始化`e.finfo`。在C++中，当你使用指针成员时，必须确保它们指向有效的内存，特别是在使用动态分配内存的情况下。

在你的`Entry`结构体中，`finfo`是一个指针，但没有看到它在`next`函数中被初始化。你需要确保在使用它之前为它分配内存。

以下是一些可能的解决方案：

1. **在`next`函数中初始化`finfo`**：
   
   确保在调用`apr_dir_read`之前，`e.finfo`指向有效的`apr_finfo_t`对象：

   ```cpp
   Entry * Iterator::next(Entry & e)
   {
       if (e.finfo == nullptr)
       {
           e.finfo = new apr_finfo_t;
       }

       apr_int32_t wanted = APR_FINFO_LINK | APR_FINFO_NAME | APR_FINFO_TYPE;
       apr_status_t res = ::apr_dir_read(e.finfo, wanted, handle_);
       
       // No more entries
       if (APR_STATUS_IS_ENOENT(res))
       {
           delete e.finfo;
           e.finfo = nullptr;
           return NULL;
       }
       
       if (res != 0)
       {
           CHECK(res == APR_INCOMPLETE) 
               << "Couldn't read next dir entry." 
               << " Error code: " << APR_TO_OS_ERROR(res);
           CHECK(((e.finfo->valid & wanted) | APR_FINFO_LINK) == wanted) 
               << "Couldn't retrieve all fields. Valid mask=" << e.finfo->valid; 
       } 

       e.type = (e.finfo->filetype == APR_DIR) ? Directory::Entry::DIRECTORY 
                                               : Directory::Entry::FILE;
       e.path = e.finfo->name;                               

       // Skip '.' and '..' directories
       if (e.type == Directory::Entry::DIRECTORY && 
          (e.finfo->name == std::string(".") || e.finfo->name == std::string("..")))
       {
           return next(e);
       }
       else
       {
           return &e;
       }
   }
   ```

2. **在构造函数中初始化`finfo`**：
   
   你可以在`Entry`结构体的构造函数中初始化`finfo`，确保每个`Entry`对象在创建时都分配了内存：

   ```cpp
   struct Entry
   {
       enum Type { FILE, DIRECTORY, LINK };

       Type type;
       std::string path;
   #ifndef PF_PLATFORM_LINUX
       apr_finfo_t* finfo;

       Entry() : finfo(new apr_finfo_t) {}
       ~Entry() { delete finfo; }
   #endif
   };
   ```

3. **使用智能指针**：
   
   使用智能指针可以自动管理内存，避免手动分配和释放内存的复杂性：

   ```cpp
   #include <memory>

   struct Entry
   {
       enum Type { FILE, DIRECTORY, LINK };

       Type type;
       std::string path;
   #ifndef PF_PLATFORM_LINUX
       std::unique_ptr<apr_finfo_t> finfo;

       Entry() : finfo(std::make_unique<apr_finfo_t>()) {}
   #endif
   };
   ```

   然后在`next`函数中，你不需要手动分配和释放内存，智能指针会自动处理：

   ```cpp
   Entry * Iterator::next(Entry & e)
   {
       apr_int32_t wanted = APR_FINFO_LINK | APR_FINFO_NAME | APR_FINFO_TYPE;
       apr_status_t res = ::apr_dir_read(e.finfo.get(), wanted, handle_);
       
       // No more entries
       if (APR_STATUS_IS_ENOENT(res))
       {
           return NULL;
       }
       
       if (res != 0)
       {
           CHECK(res == APR_INCOMPLETE) 
               << "Couldn't read next dir entry." 
               << " Error code: " << APR_TO_OS_ERROR(res);
           CHECK(((e.finfo->valid & wanted) | APR_FINFO_LINK) == wanted) 
               << "Couldn't retrieve all fields. Valid mask=" << e.finfo->valid; 
       } 

       e.type = (e.finfo->filetype == APR_DIR) ? Directory::Entry::DIRECTORY 
                                               : Directory::Entry::FILE;
       e.path = e.finfo->name;                               

       // Skip '.' and '..' directories
       if (e.type == Directory::Entry::DIRECTORY && 
          (e.finfo->name == std::string(".") || e.finfo->name == std::string("..")))
       {
           return next(e);
       }
       else
       {
           return &e;
       }
   }
   ```

**第2、第3种方法才是推荐用法**

## 2、动态库的pdb文件，才能debug进动态库的源码

我目前是专门弄了一个dll文件夹，把需要加载的动态库相关的东西放进去，所以每次动态库编译好要记得重新copy一下

## 3、之前C动态库一直出现，unresolved external symbol的原因是C库也得extern ”C“

## 4、为什么C语言动态库导出函数，也得用extern ”C“

在C语言中，使用 `extern "C"` 的主要原因是为了兼容C++，尤其是在混合编程环境中（即C和C++代码混合使用的情况下）。具体原因如下：

### 1. 名称修饰（Name Mangling）

C++编译器在编译过程中会对函数名进行修饰（name mangling），以支持函数重载和其他C++特性。这意味着同一个函数在C和C++中的符号名称可能不同。例如，假设有一个C++函数：

```cpp
void my_function(int a);
```

在C++中，编译器可能会将其修饰为类似 `_Z11my_functioni` 这样的符号名称。而在C中，函数名不会被修饰，直接是 `my_function`。

当你在C++中使用 `extern "C"` 声明一个函数时，编译器会使用C语言的名称修饰规则，从而确保函数名在C和C++中一致。

### 2. 动态库的兼容性

如果你编写一个动态库（DLL或共享库），并希望该库既能被C程序调用，也能被C++程序调用，那么在C++代码中导出函数时使用 `extern "C"` 是必要的。这样可以确保C++编译器不会对函数名进行修饰，使得C程序能够正确地找到并调用这些函数。

### 示例

假设你有一个C语言动态库，包含以下函数：

```c
// mylibrary.h
#ifndef MYLIBRARY_H
#define MYLIBRARY_H

#ifdef __cplusplus
extern "C" {
#endif

void my_function();

#ifdef __cplusplus
}
#endif

#endif // MYLIBRARY_H
```

```c
// mylibrary.c
#include "mylibrary.h"
#include <stdio.h>

void my_function() {
    printf("Hello from the library!\n");
}
```

在这个示例中，`extern "C"` 确保了 `my_function` 在C和C++中都使用相同的符号名称。

### 使用CMake构建

假设你有一个C++主程序调用这个C语言动态库：

```cpp
// main.cpp
#include "mylibrary.h"

int main() {
    my_function();
    return 0;
}
```

#### CMakeLists.txt

```cmake
# CMakeLists.txt for library
cmake_minimum_required(VERSION 3.10)
project(MyLibrary C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_BUILD_TYPE Debug)

add_library(mylibrary SHARED mylibrary.c)
```

```cmake
# CMakeLists.txt for main program
cmake_minimum_required(VERSION 3.10)
project(MyExecutable CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)

add_executable(main main.cpp)
target_link_libraries(main mylibrary)
```

### 构建和运行

1. **构建动态库**：

```sh
mkdir build_library
cd build_library
cmake ..
cmake --build .
```

2. **构建主程序**：

```sh
mkdir build_main
cd build_main
cmake ..
cmake --build .
```

3. **运行主程序**：

```sh
./main
```

### 总结

在C语言动态库中使用 `extern "C"` 是为了确保在C++中调用这些函数时，函数名不会被C++编译器修饰，从而保证C和C++代码的兼容性。这在混合编程环境中尤其重要，确保你的动态库能够被不同语言的程序正确调用。



## 15、/SUBSYSTEM:WINDOWS和/SUBSYSTEM:CONSOLE 有什么区别

`/SUBSYSTEM:WINDOWS` 和 `/SUBSYSTEM:CONSOLE` 是链接器的选项，用来告诉操作系统程序的运行模式。它们的区别主要体现在**程序入口点**、**控制台窗口**、和**用途**上：

------

### **1. /SUBSYSTEM:CONSOLE**

- **用途**： 用于控制台应用程序，例如命令行工具、脚本执行器等。
- **程序入口点**： 默认入口点是 `main` 或 `wmain`。
- **控制台窗口**：
  - 程序启动时，系统会自动分配一个控制台窗口。
  - 输出到标准输出 (`stdout`) 和标准错误 (`stderr`) 会直接显示在控制台上。
- **典型场景**： 适合需要与用户进行文本交互的程序，比如 CLI 工具或调试工具。

------

### **2. /SUBSYSTEM:WINDOWS**

- **用途**： 用于 Windows GUI 应用程序，例如图形界面程序或服务程序。
- **程序入口点**： 默认入口点是 `WinMain` 或 `wWinMain`，这两个函数包含图形界面应用所需的消息循环。
- **控制台窗口**：
  - 程序启动时不会分配控制台窗口。
  - 如果程序调用控制台相关函数（如 `printf`），除非手动附加控制台，否则不会有任何输出。
- **典型场景**： 适合需要图形界面的程序，如 Windows 桌面应用程序。

------

### **关键区别对比**

| 特性                  | /SUBSYSTEM:CONSOLE     | /SUBSYSTEM:WINDOWS           |
| --------------------- | ---------------------- | ---------------------------- |
| **入口点函数**        | `main` 或 `wmain`      | `WinMain` 或 `wWinMain`      |
| **默认控制台窗口**    | 是                     | 否                           |
| **标准 I/O 输出行为** | 可直接输出到控制台     | 需要手动附加控制台才能输出   |
| **适用场景**          | 命令行工具、后台任务等 | 图形界面应用程序、服务程序等 |

------

### **如何选择**

1. **使用 `/SUBSYSTEM:CONSOLE`**：
   - 当你的程序是一个命令行工具或需要控制台进行输入/输出时。
   - 示例：`git`, `ping`, `python` 等。
2. **使用 `/SUBSYSTEM:WINDOWS`**：
   - 当你的程序是一个图形界面应用，不需要默认控制台窗口。
   - 示例：`notepad`, `explorer` 等。

------

### **额外注意事项**

1. **动态控制台输出**： 如果你用 `/SUBSYSTEM:WINDOWS` 构建一个 GUI 应用，但仍需要在某些情况下输出到控制台，可以使用以下方式动态附加控制台：

   ```c
   AllocConsole();
   freopen("CONOUT$", "w", stdout);
   printf("Hello, Console!\n");
   ```

2. **服务程序**： 对于后台服务程序，通常也使用 `/SUBSYSTEM:WINDOWS`，因为它们不需要控制台窗口。

3. **混合场景**： 如果你需要同时支持 GUI 和控制台模式，可以在代码中动态检测是否需要附加控制台，并选择性地调用相关代码。

总结来说，选择 `CONSOLE` 或 `WINDOWS` 主要取决于程序是否需要控制台以及应用的运行环境。

## 20、通过编译好的exe文件直接启动，freeconsole可以将控制台终端关闭，但是在vs2019里启动exe文件，在debug的时候，freeconsole没办法实时将控制台终端关闭

在 Visual Studio 中调试时，`FreeConsole` 无法实时关闭控制台窗口的原因是，**调试器会附加到进程并管理其输出**。即使你的程序调用了 `FreeConsole`，调试器依然控制着控制台窗口，这会干扰 `FreeConsole` 的行为。

------

### **问题原因**

1. **调试器控制**：当在 Visual Studio 中运行程序时，调试器会附加到控制台窗口，即使 `FreeConsole` 成功释放了控制台，调试器的附加状态可能会重新激活或阻止关闭控制台。
2. **附加状态**：Visual Studio 在调试模式下启动控制台程序时，自动附加了控制台来捕获输出，这会影响 `FreeConsole` 的操作效果。

------

### **解决方案**

以下方法可以使 `FreeConsole` 在调试模式下有效：

------

#### **方法 2：通过外部终端启动调试**

在 Visual Studio 中设置外部终端运行程序，以避免调试器附加控制台窗口：

1. 打开项目的属性窗口。
2. 转到 **Configuration Properties -> Debugging**。
3. 将 **Console** 设置为 **External Terminal**。
4. 启动调试，程序将在外部终端中运行，这样调用 `FreeConsole` 后可以正常关闭控制台。

------

#### **方法 3：在 Release 模式下测试**

调试模式下，控制台与调试器绑定较紧。通过 Release 模式运行独立的 `.exe` 文件，控制台不会受到调试器干扰，`FreeConsole` 能正常工作。

------

#### **方法 4：在特定情况下调用 `FreeConsole`**

在调试模式中增加判断，仅在非调试环境下调用 `FreeConsole`：

```c
#include <windows.h>
#include <stdio.h>

int main() {
    printf("Hello, Console!\n");

#ifdef _DEBUG
    printf("Debug mode: Console will not be freed.\n");
#else
    FreeConsole();
#endif

    // 模拟程序后续运行
    Sleep(5000);

    return 0;
}
```

------

### **总结**

- Visual Studio 调试器的附加行为会干扰 `FreeConsole` 的正常运行。
- 最直接的解决方案是通过 **Release 模式** 或 **外部终端** 运行程序，避免调试器的干扰。
- 如果必须在调试模式下运行，可以手动分离调试器附加状态，但这会导致调试器无法继续跟踪程序。

## 25、visual studio工程右键设置configuration properties却可以将linker-system-subsystem设置为空

在 Visual Studio 的工程设置中，将 `Linker -> System -> Subsystem` 设置为空的确是可以的，但这通常是不建议的，因为这样做可能导致链接器无法正确设置程序的运行模式，甚至可能生成无法运行的可执行文件。

------

### 30、**为什么 Visual Studio 允许 Subsystem 为空？**

1. **默认行为**： 如果你不手动设置 `Subsystem`，链接器会尝试根据程序的入口点推断出适合的 `Subsystem` 类型：
   - 如果入口点是 `main` 或 `wmain`，链接器假定为 `/SUBSYSTEM:CONSOLE`。
   - 如果入口点是 `WinMain` 或 `wWinMain`，链接器假定为 `/SUBSYSTEM:WINDOWS`。
2. **灵活性**： 在某些特殊情况下，开发者可能希望通过命令行或自定义脚本控制 `Subsystem` 的设置，而不是通过 Visual Studio 的图形界面。因此，Visual Studio 提供了不显式指定 `Subsystem` 的选项。

------

### **将 Subsystem 设置为空会发生什么？**

- **成功推断**： 如果程序的入口点符合链接器的推断规则（如 `main` 对应 `CONSOLE` 或 `WinMain` 对应 `WINDOWS`），程序可以正常构建并运行。
- **推断失败**： 如果链接器无法推断出合适的 `Subsystem`，会报错或生成一个无法运行的程序。例如：
  - 链接器提示 `unresolved external symbol: _main` 或 `_WinMain@16`。
  - 生成的程序运行时会立即崩溃，或无法启动。

------

### **是否可以安全将 Subsystem 留空？**

- **可以留空的情况**：
  - 你完全依赖链接器根据入口点推断 `Subsystem`。
  - 程序的入口点符合默认推断规则（如 `main` 对应 `CONSOLE` 或 `WinMain` 对应 `WINDOWS`）。
- **不建议留空的情况**：
  - 如果你需要明确控制程序的运行模式（比如动态切换 Subsystem）。
  - 如果程序具有非标准入口点（例如，自定义的 `_start` 或 `DllMain`）。

------

### **推荐设置 Subsystem 的方法**

1. **明确指定**： 在 Visual Studio 中明确设置 Subsystem，可以避免不必要的推断错误：

   - 如果是控制台程序，设置为 `/SUBSYSTEM:CONSOLE`。
   - 如果是图形界面程序，设置为 `/SUBSYSTEM:WINDOWS`。

2. **手动设置**： 如果需要手动修改，打开 `Configuration Properties -> Linker -> System`，选择适当的 Subsystem。

3. **CMake 工程**： 在 `CMakeLists.txt` 中可以通过以下方式设置：

   ```cmake
   set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS "/SUBSYSTEM:CONSOLE")
   ```

------

### **总结**

虽然 Visual Studio 允许 `Subsystem` 为空，但为了更稳定的构建和运行，建议明确设置。只有在确保程序入口点符合默认推断规则时，才可以安全地留空。

## 30、最终在debug时关闭console的终极解决方案

### 真正的解决方案

- tools-options-debugging-general-automatically close the console when debugging stops
- vs2019要自己设置，vs2015是自动设置了在调试停止时关闭控制台窗口
- 真正影响的不是设置SubSystem为空，而是automatically close the console when debugging stops

### 配置属性-链接器-子系统设置为空，也可以正常在debug时通过FreeConsole将console窗口关闭

[FreeConsole 函数 - Windows Console | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/console/freeconsole)

[“链接器”属性页 | Microsoft Learn](https://learn.microsoft.com/zh-cn/cpp/build/reference/linker-property-pages?view=msvc-170)

进程可以使用 **FreeConsole** 函数从其控制台分离出来。 如果其他进程共享该控制台，则不会销毁控制台。

- 在vs2015中，子系统设置默认就是空
- 在vs2019中，子系统设置默认是Console (/SUBSYSTEM:CONSOLE)

```
SubSystem
/SUBSYSTEM 选项告知操作系统如何运行 .exe 文件。 子系统的选择会影响链接器将选择的入口点符号（或入口点函数）。

选择项

未设置 - 未设置子系统。
控制台 - Win32 字符模式应用程序。 操作系统为控制台应用程序提供控制台。 如果定义了 main 或 wmain，则 CONSOLE 为默认值。
Windows - 应用程序不需要控制台，可能是因为它会创建自己的窗口以与用户交互。 如果定义了 WinMain 或 wWinMain，则 WINDOWS 为默认值。
本机 - Windows NT 的设备驱动程序。 如果指定了 /DRIVER:WDM，则 NATIVE 为默认值。
EFI 应用程序 - EFI 应用程序。
EFI 启动服务驱动程序 - EFI 启动服务驱动程序。
EFI ROM - EFI ROM。
EFI 运行时 - EFI 运行时。
POSIX - 与 Windows NT 中的 POSIX 子系统一起运行的应用程序。
```

> 最终：
>
> - subsystem为空，debug调试器就不会影响控制台console，freeconsole就能正常关闭console
> - cmake编译就是没办法把subsystem设置为空
> - 但是visual studio工程右键设置configuration properties却可以将linker-system-subsystem设置为空