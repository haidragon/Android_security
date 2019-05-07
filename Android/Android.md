# Android

## Android生态圈
谷歌、硬件厂商（cpu、系统芯片、设备制造商）、移动通信运营商（定制机）、定制ROM、用户（消费者、高级用户、安全研究人员）
安卓安全权威攻防指南 “要想成为一名成功的安全研究人员，需要对编程语言、操作系统内部和安全概念有深刻的理解。大多数安全研究人员能够使用多种编程语言开发、阅读与编写代码。对他们而言，花时间深入研究安全概念，理解操作系统内部远离，以及获取技术前沿信息都是非常普遍的事情”

## Android平台架构

1 System Apps 
2 Java API Framework 
3.1 Native C/C++ Libraries 
3.2 Android Runtime 
4 Hardware Abstraction Layer 
5 Linux Kernel 
6 Power Management

### 1 System Apps 
### 2 Java API Framework 
### 3.1 Native C/C++ Libraries 
### 3.2 Android Runtime 
### 4 Hardware Abstraction Layer 
### 5 Linux Kernel 
### 6 Power Management 

### Android应用层
主要的应用组件：
AndroidManifest、Intent、Activity、BroadcastReceiver、Service、Content Provider。
#### AndroidManifest
* 唯一的应用包名及版本信息
* Activity、Service、BroadcastReceiver和插桩定义
* 权限定义（应用请求、应用自定义的权限）
* 关于应用使用并一起打包的外部程序库信息
* 其他支持性指令，比如共用的UID信息、首选的安装位置和UI信息
由开发环境自动生成（比如Eclipse 或者 Android Studio）

#### Intent
一种消息对象，其中包含要执行操作的相关信息，将执行操作的目标组件信息（可选），以及其他一些（对接收方可能非常关键的）标识位或支持行信息。比如在一个邮件中点击链接来启动浏览器。
这个类，类似于IPC or RPC。如果涉及权限，Android运行时将作为一个参考监视器，对Intent执行权限检查。
Manifest文件中声明特定的组件时，可以指明一个Intent Filter，来定义端点处理的标准。

#### Activity
Activity是一种面向用户的应用组件或用户界面。基于Activity基类，包括一个窗口和相关的UI元素。Activity底层管理由被称为Activity管理服务的组件进行处理。这个组件也处理应用之间或应用内部用于调用Activity的发送Intent。

##### activity中的常见配置：


Lable属性：
Activity页面的标题，界面的名字，如果此界面被创建快捷方式，则快捷方式的名字就是lable值
Name属性：
指定的值为:包名.Activity类名。
包名如果与mainfest的package一致，可以用“.”代替。或者不写
Intent-filter子节点：
添加意图过滤，可以通过隐式意图启动。
可以在桌面生成快捷方式，应用程序的入口
Icon属性：
指定应用程序的图标
android：theme属性：指定主题
android：theme="@android:style/Theme.Dialog"
android：exported
是否允许外部程序调用
android:exported 是Android中的四大组件 Activity，Service，Provider，Receiver 四大组件中都会有的一个属性。
总体来说它的主要作用是：是否支持其它应用调用当前组件。 
默认值：如果包含有intent-filter 默认值为true; 没有intent-filter默认值为false。
* ref
https://blog.csdn.net/watermusicyes/article/details/46460347
 
#### BroadcastReceiver
在应用希望接收到一个匹配某种特定标准的隐式Intent时出现。例如，一个应用想要接受与短信息关联的Intent，它需要在Manifest文件中注册一个Receiver，使用Intent Filter来匹配动作。

#### Service
后台运行而无需用户界面的应用组件，用户不用直接与Service所属应用交互。

#### Content Provider
为各种通用、共享的数据存储提供的结构化访问接口。

### Android框架层
应用和运行时之间的连接纽带，Android框架层提供执行通用任务的部件--程序包及其类。这些任务可能包括管理UI元素、访问共享数据存储，以及在应用组件中传递消息等。通常框架层程序包位于android.\*名字空间中
框架层的管理者
* Activity管理器
* 视图系统
* 程序包管理器
* 电话管理器
* 资源管理器
* 位置管理器
* 通知管理器

### DalvikVM
Dalvik是Google公司自己设计用于Android平台的虚拟机。Dalvik经过优化，使其更适合Android平台。具体优点会在下面和JVM进行比较时说明。
2014年6月谷歌I/O大会，Android L 改动幅度较大，Google将直接删除Dalvik，代替它的是传闻已久的ART。
而ART又和Dalvik有什么联系和区别呢？
JVM、DalvikVM、ART

* 先对Dalvik以及ART做简单介绍：

什么是Dalvik：

Dalvik是Google公司自己设计用于Android平台的Java虚拟机。它可以支持已转换为.dex(即Dalvik Executable)格式的Java应用程序的运行，.dex格式是专为Dalvik应用设计的一种压缩格式，适合内存和处理器速度有限的系统。Dalvik经过优化，允许在有限的内存中同时运行多个虚拟机的实例，并且每一个Dalvik应用作为独立的Linux进程执行。独立的进程可以防止在虚拟机崩溃的时候所有程序都被关闭。

 

* 什么是ART：

ART代表AndroidRuntime，Dalvik是依靠一个Just-In-Time(JIT)编译器去解释字节码，运行时编译后的应用代码都需要通过一个解释器在用户的设备上运行，这一机制并不高效，但让应用能更容易在不同硬件和架构上运行。

ART则完全改变了这种做法，在应用安装的时候就预编译字节码到机器语言，这一机制叫Ahead-Of-Time(AOT)预编译。在移除解释代码这一过程后，应用程序执行将更有效率，启动更快。



* Dalvik与JVM的区别

（1）Dalvik指令集是基于寄存器的架构，执行特有的文件格式——dex字节码（适合内存和处理器速度有限的系统）。而JVM是基于栈的。相对于基于栈的JVM而言，基于寄存器的Dalvik VM实现虽然牺牲了一些平台无关性，但是它在代码的执行效率上要更胜一筹。

（2）每一个Android 的App是独立跑在一个VM中的。因此一个App crash只会影响到自身的VM，不会影响到其他。Dalvik经过优化，允许在有限的内存中同时运行多个虚拟机的实例，并且每一个 Dalvik应用作为一个独立的Linux进程执行。

 

* Dalvik与ART的区别

（1）在Dalvik下，应用每次运行都需要通过即时编译器（JIT）将字节码转换为机器码，即每次都要编译加运行，这虽然会使安装过程比较快，但是会拖慢应用的运行效率。而在ART 环境中，应用在第一次安装的时候，字节码就会预编译（AOT）成机器码，这样的话，虽然设备和应用的首次启动（安装慢了）会变慢，但是以后每次启动执行的时候，都可以直接运行，因此运行效率会提高。

（2）ART占用空间比Dalvik大（原生代码占用的存储空间更大，字节码变为机器码之后，可能会增加10%-20%），这也是著名的“空间换时间大法"。

（4）预编译也可以明显改善电池续航，因为应用程序每次运行时不用重复编译了，从而减少了 CPU 的使用频率，降低了能耗。

## 用户空间原生代码层
### 程序库
一些so文件
### 核心服务
建立基本操作系统环境的服务与Android原生组件。这些服务包括初始化用户控件的服务、提供关键调试功能的服务（adbd、debugggerd等）

## PackageManager
管理应用程序包,通过PackageManager，我们就可以获取应用程序信息。
AndroidManifest.xml是Android应用程序中最重要的文件之一。它是Android程序的全局配置文件，是每个 android程序中必须的文件。它位于我们开发的应用程序的根目录下，描述了package中的全局数据，包括package中暴露的组件 （activities, services, 等等），以及他们各自的实现类，各种能被处理的数据和启动位置等重要信息。 
PackageManager获取的信息即来自AndroidManifest.XML。

### 一、PackageManager的功能：
	1、安装，卸载应用 
	2、查询permission相关信息 
	3、查询Application相关信息(application，activity，receiver，service，provider及相应属性等） 
	4、查询已安装应用 
	5、增加，删除permission 
	6、清除用户数据、缓存，代码段等 

