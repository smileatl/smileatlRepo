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

## 10、配置属性-链接器-子系统设置，为空，才能正常在debug时通过FreeConsole将console窗口关闭

[FreeConsole 函数 - Windows Console | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/console/freeconsole)

[“链接器”属性页 | Microsoft Learn](https://learn.microsoft.com/zh-cn/cpp/build/reference/linker-property-pages?view=msvc-170)

进程可以使用 **FreeConsole** 函数从其控制台分离出来。 如果其他进程共享该控制台，则不会销毁控制台。如果设置了console，操作系统为控制台应用程序提供控制台，则不会销毁该控制台。

- 在vs2015中，子系统设置默认就是空
- 在vs2019中，子系统设置默认却是Console (/SUBSYSTEM:CONSOLE)

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



> 最终：试来试去还是不行，cmake编译就是没办法把subsystem设置为空