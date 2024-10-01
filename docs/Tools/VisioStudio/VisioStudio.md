## 1、快捷键

`ctrl+,`可以快速查找文件

`ctrl+L`可以快速剪切一行

## 5、部分格式编码乱掉问题如何快速解决

将文件删除，通过文件资源管理器右键新建文件的方式新增.cpp或.h文件

然后在visio studio中通过右键add existing item的方式，把文件加回来



## 10、visio studio中references和dependencies的区别

当在 Visual Studio 中开发项目时，以下四个概念在管理项目依赖关系和构建过程中起着重要的作用：

1. "References"（引用）：它用于管理项目对其他程序集的依赖关系。通过添加引用，你可以在项目中使用其他项目或程序集中的类型和成员。这些引用通常用于编译时解析，以确保在构建项目时可以访问所需的依赖项。（**Solution下的project互相引用，不使用就不需要引用，一般都是Solution下真正存在的project，而不是其他下载下来的编译好后的库**）

2. "Build Dependencies"（构建依赖）：它用于指定项目之间的构建顺序和依赖关系。通过设置项目之间的构建依赖关系，你可以确保在构建解决方案时，依赖的项目会在它们被依赖的项目之前进行构建。这对于确保正确的构建顺序和避免构建错误非常重要。（**Solution下project互相之间的构建依赖，一个project必须晚于其依赖项的构建，一般都是Solution下真正存在的project，而不是其他下载下来编译好后的后库**）

3. "General -> Additional Include Directories"（附加包含目录）：它是一个设置，用于指定编译器在搜索头文件时要查找的附加目录。通过将头文件的路径添加到这个设置中，编译器可以找到并包含所需的头文件。（**指定搜索头文件的目录，是会有下载下来的编译好后的库**）

4. "Linker -> Input"（链接器输入）：它是一个设置，用于指定链接器在链接过程中要使用的库文件。通过将库文件的路径添加到这个设置中，链接器可以找到并链接所需的库文件。（**链接库文件，是会有下载下来的编译好后的库**）

这些概念之间的关系和区别如下：

- "References" 和 "Build Dependencies" 都涉及项目之间的依赖关系，但从不同的角度管理这些依赖关系。"References" 管理项目对其他程序集的依赖关系，而 "Build Dependencies" 管理项目之间的构建顺序和依赖关系。

- "References" 和 "Build Dependencies" 都是在解决方案资源管理器中设置的，以确保在构建解决方案时正确处理依赖关系。

- "General -> Additional Include Directories" 和 "Linker -> Input" 是针对编译和链接过程中的文件路径的设置。"General -> Additional Include Directories" 设置用于指定编译器在搜索头文件时要查找的附加目录，而 "Linker -> Input" 设置用于指定链接器在链接过程中要使用的库文件。

- "General -> Additional Include Directories" 和 "Linker -> Input" 是**与文件路径相关的设置**，而 "References" 和 "Build Dependencies" 是**用于管理项目之间的依赖关系的机制**。

总结：
- "References" 管理项目对其他程序集的依赖关系。
- "Build Dependencies" 管理项目之间的构建顺序和依赖关系。
- "General -> Additional Include Directories" 设置用于指定编译器在搜索头文件时要查找的附加目录。
- "Linker -> Input" 设置用于指定链接器在链接过程中要使用的库文件。

希望这次解答对你有帮助。如果还有其他问题，请随时提问。