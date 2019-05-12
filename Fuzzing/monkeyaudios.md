# 转向ffmeg和chrome以及qq音乐
	ape.c
	https://github.com/FFmpeg/FFmpeg/blob/master/libavformat/ape.c
	ffmpeg的libavformat的ape.c直接使用monkey（看看是否还继续使用）
	有关于ffmeg的bounty（一年没更新了）
	https://hackerone.com/ibb-data
	ffmeg上了hackone
	https://hackerone.com/ffmpeg

	使用FFMPEG作为内核视频播放器：
	Mplayer，ffplay，射手播放器，暴风影音，KMPlayer，QQ影音...

## 下一步
* ffmpeg、qq音乐是否还支持ape，chrome使用了ffmpeg哪些部分
* 分析crash，输出crash报告，fix，继续fuzz

1. qq音乐也有ape，但是不是这个库，但是可能漏洞模式一样。
我还是分析这个库吧先
2. ffmpeg

apetag.c == console.cpp 

ffmpeg
A complete, cross-platform solution to record, convert and stream audio and video.

ffmpeg -i input.mp4 output.avi

.
======================
是否可以直接crash
	sudo apt-get install ffmpeg
	test 了 3个 不能直接crash ffmpeg
	说明ffmpeg做了检测
	test 了 fuzz_input里的文件 不能被ffmpeg 解析
	所以接下来 需要改进seeds
======================

改进seeds
======================
下载ape？曾经下载过，没有。如果没有，用其他格式转成ape
小一点，3个就够了
小一点 随便的，以及大的
重新编译./mac 重新进行fuzz 进行尝试
就边看边审计，看看每一个输入能够控制到的变量
是否在fuzz过程中，都达到过它们的边界值
如果达到边界值，会产生什么后果

种子质量问题
就是尽可能让种子差异化大不同的参数，不同的transformer，不同的源文件格式去进行转换，就可以得到 varieties of seeds
熟悉一波ffmpeg
控制输入
下载pcm mp3 avi wav格式
转换成ape格式
https://www.poweriso.com/tutorials/convert-to-ape.htm
======================
转换成功，开始fuzz mac
当时mac怎么fuzz... 来着...
先用AFL编译mac，然后设置输入
afl-fuzz -m none -i fuzz_in/ -o fuzz_out/ ./mac @@

size太大。
优化afl-fuzz 
	修改源码
	定位报错信息
	[-] PROGRAM ABORT : Test case 'fuzz_in//1.ape' is too big (19.1 MB, limit is 1.00 MB)
         Location : read_testcases(), afl-fuzz.c:1472
使用

so wired,,,,input不少了，但是还是最终只跑一个路径 (odd,check syntax) 
下一步，增加了一个解压的参数 -d
fuzz 两天 34个crash 都被ffmpeg patch了
是在那里patch的？ 调试ffmpeg  应该是ffmpeg做了检测了

然后 改进 fuzz
。。。。。

我可以验证一下是否可以直接crash
so stubid 。
下载ffmpeg 用afl进行编译

（我为什么要fuzz monkey audio？ 我想先跑出好多crash，再看那边行不行。 但是 直接fuzz ffmpeg不就解决了吗.... 问题在于 惯性思维， 以后做完了事情。要反思三次 并写出来 我做对了么，或者是否可以优化）

昨晚今天了fuzz。但是白fuzz了的感觉。都timeout了。 
我需要进行改进，种子上面进行改进。
找1M以下的音乐格式
[～，785] [326,0]

挖洞
需不需要搞明白 ffmpeg里ape.c
带着这个问题去审计代码（审计经过的那些代码）

afl-cov

动态调试ffmpeg， 看编解码ape 经过了哪些function
审计这两个地方的代码 会有什么逻辑漏洞、二进制漏洞
demux 、 decode

### 文件格式

* struct AVFormatContext

### demux

AVFormatContext
{
	/**
     * I/O context.
     *
     * - demuxing: either set by the user before avformat_open_input() (then
     *             the user must close it manually) or set by avformat_open_input().
     * - muxing: set by the user before avformat_write_header(). The caller must
     *           take care of closing / freeing the IO context.
     *
     * Do NOT set this field if AVFMT_NOFILE flag is set in
     * iformat/oformat.flags. In such a case, the (de)muxer will handle
     * I/O in some other way and this field will be NULL.
     */
	AVIOContext *pb;
}


### decode
# 联系方式
	https://monkeysaudio.com/contact.html
	mail@monkeysaudio.com