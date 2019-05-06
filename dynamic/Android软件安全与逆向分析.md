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
掌握Dex文件的格式
### Android程序的生成步骤
第一步：打包资源文件，生成R.java文件
  使用打包资源的工具aapt下的Resource.cpp文件中的buildResources()函数。
  这个函数首先检查AndroidManifest.xml的合法性，然后对res目录下的资源子目录进行处理。处理的函数为makeFileResources()。处理的内容包括资源文件名的合法性检查，向资源表table添加条目等，处理完后调用compileResourceFile（）函数编译res与asserts目录下的资源并生成resources.arsc文件。
  完成资源编译后，接下来调用compileXmlFile（）函数对res目录对子目录下的xml文件分别进行编译，这样处理过的xml文件就被简单的加密了。
第二步：处理aidl文件，生成相应的Java文件
第三步：编译工程源代码，生成相应的class文件
第四步：转换所有的class文件，生成class.dex文件
第五步：打包生成APK文件
第六步：对APK文件进行签名
第七步：对签名后的APK文件进行对其处理。
### Android程序的安装流程
1.系统程序安装
2.Android市场安装
3.ADB工具安装
4.手机自带安装
第一种由开机时启动的PackageManagerService服务完成，这个服务在启动时会扫描系统程序目录/system/app并重新安装所有程序。
第四种调用Android系统的软件包packageinstall.apk
### dex文件格式
在Android4.0 Dalvik/docs目录下提供了一份文档 dex-format。html里面详细介绍了dex文件格式以及使用到的数据结构。

## 静态分析Android程序
静态分析：不运行代码的情况下，采用词法分析、语法分析等各种技术手段对程序文件进行扫描从而生成程序的反汇编代码，然后阅读反汇编代码来掌握程序功能的一种技术。
### 快速定位Android程序的关键代码
1.AndroidManifest.xml 
2.程序主Activity（程序入口） 
绝大多数，看Activity中的android.intent.category.LAUNCHER 以及  android.intent.action.MAIN 
3.需要重点关注的Application类（破解点常在的位置） 
### 如何定位关键代码之六脉神剑 
1.信息反馈：根据程序运行时给出的反馈信息作为突破口寻找关键代码 
2.特种函数法： 
3.顺序查看发：病毒分析时常用 
4.代码注入法：解密程序数据 
5.栈跟踪法：动态调试方法，查看函数调用序列 
6.MethodProfiling（方法剖析），热点分析和性能优化 
### Android程序中的类 TODO
1.内部类
2.监听器
3.注解类
4.自动生成的类
### 反编译后的smali代码 TODO
1.循环语句
2.switch
3.try/catch
### 使用IDA Pro静态分析Android程序 TODO（IDA Pro 权威指南）
### 恶意软件分析工具包--Androguard
### 集成分析环境--santoku
   实质上是一套定制的Ubuntu 12.04系统镜像
  1.集成了大量主流Android程序分析工具
  2.集成移动设备取证工具。
  3.集成渗透测试工具
  4.集成网络数据分析工具
  5.beta阶段，充满活力
## 基于Android的ARM汇编语言基础--逆向原生 TODO 学习arm语言
## AndroidNDK程序逆向分析
  Android NDK “安卓原生开发套件”，可以将原生C、C++代码的强大功能和Android应用的图形界面结合在一起，解决软件的跨平台问题。通过使用该工具，一些应用程序能直接通过JNI调用与CPU打交道而使性能得到提升。
  从R8版本开始，支持生产X86、MIPS、ARM三种架构的原生程序。TODO 学习开发JNI
## 动态调试Android程序 TODO 
## Android软件的破解技术
## Android程序的反破解技术
## Android系统攻击与防范

