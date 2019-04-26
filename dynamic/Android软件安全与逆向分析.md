# Android软件安全与逆向分析

## JNI（Java Native Interface）
 JNI是一个协议，这个协议用来沟通java代码和外部的本地代码(c/c++)外部的c/c++代码也可以调用java代码

堆内存和栈内存的概念
栈内存：系统自动分配和释放，
      保存全局、静态、局部变量，
      在站上分配内存叫静态分配，
      大小一般是固定的
堆内存：程序员手动分配(malloc/new)和释放(free/java不用手动释放，由GC回收)，
      在堆上分配内存叫动态分配

## 交叉编译
1、交叉编译的概念
  交叉编译即在一个平台，编译出另一个平台能够执行的二进制代码
  主流平台有： Windows、 Mac os、 Linux
  主流处理器： x86、 arm、 mips
2、交叉编译的原理
  即在一个平台上，模拟其他平台的特性
  编译的流程： 源代码-->编译-->链接-->可执行程序
3、交叉编译的工具链
  多个工具的集合，一个工具使用完后接着调用下一个工具
4、常见的交叉编译工具
  NDK(Native Development Kit): 开发JNI必备工具，就是模拟其他平台特性类编译代码的工具
  CDT(C/C++ Development Tools): 是Eclipse开发C语言的一个插件，高亮显示C语言的语法
  Cygwin: 一个Windows平台的Unix模拟器（可以参考之前博客Cygwin简介及使用）
5、NDK的目录结构（可以在Google官网下载NDK开发工具，需要FQ）
  docs: 帮助文档
  build/tools：linux的批处理文件
  platforms：编译c代码需要使用的头文件和类库
  prebuilt：预编译使用的二进制可执行文件
  sample：jni的使用例子
  source：ndk的源码
  toolchains：工具链
  ndk-build.cmd:编译打包c代码的一个指令，需要配置系统环境变量

## JNI开发
1、编写声明native方法的Java类
2、将Java源代码编译成class字节码文件
3、用javah -jni命令生成.h头文件
4、用本地代码实现.h头文件中的函数
5、将本地代码编译成动态库
5、拷贝动态库至java.library.path本地库搜索目录下，并运行Java程序

## 如何分析Android程序
## 进入AndroidDalvik虚拟机
## Android可执行文件
## 静态分析Android程序
## 基于Android的ARM汇编语言基础--逆向原生
## AndroidNDK程序逆向分析
## 动态调试Android程序
## Android软件的破解技术
## Android程序的反破解技术
## Android系统攻击与防范

