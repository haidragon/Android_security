# Android_security

## Android的功能
* Android生态圈
TODO:
* 各个组件，存的漏洞类型，这些漏洞的利用可能性有多大，被利用之后分别会产生什么样的效果

## 语言
       c、c++、java、javascript、python、scala、smali
## 技能

* 看洞
	历史漏洞的git log、bug报告、从非 lib 目录下等

* 识洞
	代码审计

* ctf
	看着做吧
* CVE

## 分析记录

## 动态调试(dynamic)
	软件调试可以分为源码级调试与汇编级调试。源码级调试（代码审计）多用于软件开发阶段，汇编级调试也就是动态调试。

## 代码审计

* 安卓 app
	历史漏洞
    掌握漏洞所在模块或子系统，不看完整的漏洞细节描述，尝试在漏洞版本中找出对应的漏洞
    如果未能找出漏洞，去看漏洞细节描述，对比自己审计过程，看遗漏了哪一步骤
    直到相信：挖洞只是体力消耗，而非能力问题

* 项目所涉及安卓 app

## Fuzzing训练
	已公开的历史漏洞问自己，如何写fuzzer挖掘到此漏洞，如果自己不知道此漏洞，那又能挖掘到呢？不断重复训练并改进fuzzer
	甚至可以来一个议题，叫做： From open-source security to closed-source application
	然后就发现，这个方向可以一直做下去，包括组件的识别啊，版本识别啊，开源闭源对应啊，爬虫扫描啊，漏洞模式，触发路径寻找啊，inter-device fuzzing啊
	搞出个 exploit android app deep from the native world

## 漏洞信息来源
	RSS、相关博文

## 漏洞挖掘工具

## 工具与方法论沉淀
   一些漏洞可能需要人工审计，不少漏洞可以自动化Fuzzing，一些能自动化或半自动化实现的，尽量写程序自动化

## DOING

* Thor
* fk项目（移动app分析）
* monkey(1个月)
	ffmeg
	chrome
* https://github.com/B3nac/Android-Reports-and-Resources

## Mark
wrike (lib/armeabi-v7a/libnpl-tls.so,execv，Musigy::Platform::PID __fastcall Musigy::Platform::SpawnProcess,涉及到c++ name mangling ref https://blog.csdn.net/yaoyutian/article/details/55209963。类似于Jni，需要自己逆出虚表，手动调)

