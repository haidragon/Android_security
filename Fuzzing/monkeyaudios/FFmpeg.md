# FFmpeg
* https://blog.csdn.net/leixiaohua1020/article/list/2?t=1&
雷神的blog

FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。它包括了领先的音/视频编码库libavcodec等。

libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构
和读取音视频帧等功能；
libavcodec：用于各种类型声音/图像编解码,对信号或者数据流进行变换的程序；
libavutil：包含一些公共的工具函数；
libswscale：用于视频场景比例缩放、色彩映射转换；
libpostproc：用于后期效果处理；
ffmpeg：该项目提供的一个工具，可用于格式转换、解码或电视卡即时编码等；
ffsever：一个 HTTP 多媒体即时广播串流服务器；
ffplay：是一个简单的播放器，使用ffmpeg 库解析和解码，通过SDL显示；

## FFmpeg
参数中文详解
ref https://blog.csdn.net/leixiaohua1020/article/details/12751349
基于FFMPEG的音频编码器
ref https://blog.csdn.net/hy119/article/details/81632662
ref https://baike.baidu.com/item/ffmpeg/2665727?fr=aladdin
* ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
	 _______              ______________
	|       |            |              |
	| input |  demuxer   | encoded data |   decoder
	| file  | ---------> | packets      | -----+
	|_______|            |______________|      |
	                                           v
	                                       _________
	                                      |         |
	                                      | decoded |
	                                      | frames  |
	                                      |_________|
	 ________             ______________       |
	|        |           |              |      |
	| output | <-------- | encoded data | <----+
	| file   |   muxer   | packets      |   encoder
	|________|           |______________|


## libavformat
demuxer 直接处理文件格式，把里面的各项内容都找出来
## libavcodec
将demuxer提取出来的stream，以及config信息，进行byte or bit level的解码

## 源码编译ffmpeg
* 根据此来编译http://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg

神tmd编译成功了，，，

https://github.com/floyd-fuh/afl-crash-analyzer/blob/master/testcases/ffmpeg/install.sh 

CC="/usr/local/bin/afl-clang" CXX="/usr/local/bin/afl-clang++" ./configure --prefix="/home/miy1z1ki/ffmpeg_build" --pkg-config-flags="--static" --extra-cflags="-I/home/miy1z1ki/ffmpeg_build/include -c -fsanitize=address -O0 -g -v" --extra-cxxflags="-I/home/miy1z1ki/ffmpeg_build/include -c -fsanitize=address -O0 -g -v" --extra-ldflags="-L/home/miy1z1ki/ffmpeg_build/lib -fsanitize=address" --extra-libs="-lpthread -lm" --bindir="/home/miy1z1ki/bin" --enable-gpl --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libvorbis --enable-libvpx --enable-nonfree   

## ffmpeg历年漏洞
见FFmpeg漏洞.md

目的是 挖洞
搞清楚ffmpeg整体功能
ape编解码是什么流程

## FFmpeg 半拆解：
FFmpeg用于视音频编解码。
本节着重介绍FFmpeg在对ape音频进行转换时，所使用的功能以及涉及的架构。
视音频技术主要包含以下几点：封装技术，视频压缩编码技术以及音频压缩编码技术。
作为我只关注的音频来说，此处为视频播放器的简要原理。
.
								  ->视频压缩数据->视频解码->视频原始数据->
								  |									|
   数据->解协议->封装格式数据->解封装->									 -> 视音同步->
								  |									|
								  ->音频压缩数据->音频解码->音频原始数据->
编解码音频只涉及到如下

* 1.解封装的作用，就是将输入的封装格式的数据，分离成为音频流压缩编码数据和视频流压缩编码数据。封装格式种类很多，例如MP4，MKV，RMVB，TS，FLV，AVI等等，它的作用就是将已经压缩编码的视频数据和音频数据按照一定的格式放到一起。例如，FLV格式的数据，经过解封装操作后，输出H.264编码的视频码流和AAC编码的音频码流。

* 2.解码的作用，就是将视频/音频压缩编码数据，解码成为非压缩的视频/音频原始数据。音频的压缩编码标准包含AAC，MP3，AC-3等等，视频的压缩编码标准则包含H.264，MPEG2，VC-1等等。解码是整个系统中最重要也是最复杂的一个环节。通过解码，压缩编码的视频数据输出成为非压缩的颜色数据，例如YUV420P，RGB等等；压缩编码的音频数据输出成为非压缩的音频抽样数据，例如PCM数据。


* 音频编码

音频编码的主要作用是将音频采样数据（PCM等）压缩成为音频码流，从而降低音频的数据量。音频编码也是互联网视音频技术中一个重要的技术。但是一般情况下音频的数据量要远小于视频的数据量，因而即使使用稍微落后的音频编码标准，而导致音频数据量有所增加，也不会对视音频的总数据量产生太大的影响。高效率的音频编码在同等的码率下，可以获得更高的音质。

音频编码的简单原理可以参考：音频编码基本原理

近年来并未推出全新的音频编码方案，可见音频编码技术已经基本可以满足人们的需要。音频编码技术近期绝大部分的改动都是在MP3的继任者——AAC的基础上完成的。

### FFmpeg的结构与概念
我们根据官方与雷神的参考进行软件架构分析。想要分析软件的结构，应从大到小、从外向内进行分析。
所以FFmpeg在对音频文件进行编解码的时候

ffmpeg库的实用：转码

* 参考 最简单的基于FFMPEG的转码程序
* 比较复杂的转码程序可以参考ffmpeg.c，它移植到MFC下的工程：ffmpeg转码器移植VC的工程：ffmpeg for MFC

从软件功能划分软件结构

从功能结构划分工程架构
