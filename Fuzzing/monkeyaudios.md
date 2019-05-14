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

ape 除去 debug 模式 还有四个demux函数
---------
ape_probe 用 AV_RL16 取 AVProbeData 结构中 4字节 为version，取p-buf里 前8字节，MKTAG是否为'M', 'A', 'C', ' '
---------
ape_read_header 读取 AVFormatContext 结构的 s
首先用avio_tell函数同步s->pb中 avio_tell函数如下所示：
'''
static av_always_inline int64_t avio_tell(AVIOContext *s)
{
    return avio_seek(s, 0, SEEK_CUR);
}
'''
调用avio_seek，寻找s current 位置，找到同步标识位置，存入ape->junklength（int64_t）,avio_rl32 函数的功能应该是从pb读取4byte，
接下来判断 ape里 fileversion。大于3980时，读取 padding1、descriptorlength、headerlength、seektablelength、wavheaderlength、audiodatalength、audiodatalength_high、wavtaillength。
读取pb里，存取的md5值，这个文件的md5值，
然后，
'''
if (ape->descriptorlength > 52)
            avio_skip(pb, ape->descriptorlength - 52);
'''
如果ape->descriptorlength 描述的长度大于52，从 descriptorlength 指向的地方之后读取头部信息
/
读取信息如下所示
'''
	/* Read header data */
	ape->compressiontype      = avio_rl16(pb);
	ape->formatflags          = avio_rl16(pb);
	ape->blocksperframe       = avio_rl32(pb);
	ape->finalframeblocks     = avio_rl32(pb);
	ape->totalframes          = avio_rl32(pb);
	ape->bps                  = avio_rl16(pb);
	ape->channels             = avio_rl16(pb);
	ape->samplerate           = avio_rl32(pb);
'''
如果ape fileversion < 3980

'''
	ape->descriptorlength = 0;
	ape->headerlength = 32;
	ape->compressiontype      = avio_rl16(pb);
	ape->formatflags          = avio_rl16(pb);
	ape->channels             = avio_rl16(pb);
	ape->samplerate           = avio_rl32(pb);
	ape->wavheaderlength      = avio_rl32(pb);
	ape->wavtaillength        = avio_rl32(pb);
	ape->totalframes          = avio_rl32(pb);
	ape->finalframeblocks     = avio_rl32(pb);
'''
当ape fileversion 小于这么多的时候，进行一些判断与赋值操作，我猜应该是因为小于3980的 头部格式已经确定很久的原因吧。

先看 大于3980的吧 

首先，获取ape->frames sizeof(APEFrame)的内存，然后，得到ape->firstframe指向的位置，设置ape->currentframe = 0;
### ape格式
ape文件头的数据存储形式受版本号fileversion和格式标志位 formatflags影响

'''
	char			magic[4]		"MAC" ape文件标志，第四位是空格
	init16_t		fileversion 	ape版本号，其值在3800-3990之间？有check吗

	之后的数据存储结构分两种 fileversion >= 3980的和fileversion < 3980

	int16_t         	padding1                                    
	int32_t          	descriptorlength
	int32_t          	headerlength
	int32_t          	seektablelength
	int32_t          	wavheaderlength
	int32_t          	audiodatalength
	int32_t          	audiodatalength_high
	int32_t          	wavtaillength
	uint8_t          	md5[16]

	若descriptorlength > 52，需要从当前位置往后跳过(descriptorlength - 52)个字节，现阶段descriptorlength其实都等于52 

	uint16_t           compressiontype                                             压缩等级：1000-fast；2000-normal；3000-high；4000-extra high；5000-insane

	uint16_t           formatflags
	uint32_t           blocksperframe
	uint32_t           finalframeblocks
	uint32_t           totalframes
	uint16_t           bps
	uint16_t           channels
	uint32_t           samplerate

	若fileversion < 3980，当然肯定大于3800的，因为这里涉及到大量的if条件讨论，

	uint16_t           compressiontype
	uint16_t           formatflags
	uint16_t           channels
	uint16_t           samplerate
	uint32_t           wavheaderlength
	uint32_t           wavtaillength
	uint32_t           totalframes
	uint32_t           finalframeblocks

	之后的数据存储形式就和formatflags有关了，先定义几个宏，用于判断formatflags对应位上是0还是1

	#define    MAC_FORMAT_FLAG_8_BIT                           1          // is 8_bit[OBSOLETE]
	#define    MAC_FORMAT_FLAG_CRC                             2         // uses the new CRC32 error detection[OBSOLETE]
	#define    MAC_FORMAT_FLAG_HAS_PEAK_LEVEL                  4        //  uint32 nPeakLevelafter the header[OBSOLETE]
	#define    MAC_FORMAT_FLAG_24_BIT                          8         // is 24_bit[OBSOLETE]
	#define    MAC_FORMAT_FLAG_HAS_SEEK_ELEMENTS               16       // has the number of seek elements after the peak level
	#define    MAC_FORMAT_FLAG_CREATE_WAV_HEADER               32      // create the wave header on decompression (not stored)

	ape->descriptorlength = 0;
	ape->headerlength = 32;
	if (ape->formatflags & MAC_FORMAT_FLAG_HAS_PEAK_LEVEL) {
	        avio_skip(pb, 4); /* Skip the peak level */
	        ape->headerlength += 4;
	    }
	    if (ape->formatflags & MAC_FORMAT_FLAG_HAS_SEEK_ELEMENTS) {
	        ape->seektablelength = avio_rl32(pb);
	        ape->headerlength += 4;
	        ape->seektablelength *= sizeof(int32_t);
	    } else
	        ape->seektablelength = ape->totalframes * sizeof(int32_t);
	    if (ape->formatflags & MAC_FORMAT_FLAG_8_BIT)
	        ape->bps = 8;
	    else if (ape->formatflags & MAC_FORMAT_FLAG_24_BIT)
	        ape->bps = 24;
	    else
	        ape->bps = 16;
	    if (ape->fileversion >= 3950)
	        ape->blocksperframe = 73728 * 4;
	    else if (ape->fileversion >= 3900 || (ape->fileversion >= 3800  && ape->compressiontype >= 4000))
	        ape->blocksperframe = 73728;
	    else
	        ape->blocksperframe = 9216;
	    /* Skip any stored wav header */
	    if (!(ape->formatflags & MAC_FORMAT_FLAG_CREATE_WAV_HEADER))
	        avio_skip(pb, ape->wavheaderlength);
	里面有几个自定义的函数，其实已经可以猜出其意思。avio_skip是跳过字节，avio_rl32是读32bit即4字节，并用小端方式算出其值，之后还会出现avio_r8就是读一个字节。
	好了到此为止已经把fileversion的两种情况的数据存储结构分析清楚了
	ape->totalsamples = ape->finalframeblocks;
	if(ape->totalframes > 1)
	    ape->totalsamples += ape->blocksperframe * (ape->totalframes - 1);

	if(ape->seektablelength > 0){
	    ape->seekable = malloc(ape->seektablelength);
	    for(i = 0;i < ape->seektablelength / sizeof(uint32_t);i++)
	        ape->seektable[i] = avio_rl32(pb);
	    if(ape->fileversion < 3810){
	        ape->bittable = malloc(ape->totalframes);
	        for(i = 0;i < ape->totalframes;i++)
	            ape->bittable[i] = avio_r8(pb);
	    }
	}
	主要是把seektable和bittable的表项解析出来，而seektable在实现seek跳转的时候非常重要。其中pb是文件指针




'''
### decode
# 联系方式
	https://monkeysaudio.com/contact.html
	mail@monkeysaudio.com