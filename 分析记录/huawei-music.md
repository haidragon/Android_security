# huawei-music

为期一个月fuzz，第一天

360显危镜
http://appscan.360.cn/app/4775f769b3e7b0e72fde86035986dcde/report/

activity绑定browserable与自定义协议
activity设置“android.intent.category.BROWSABLE”属性并同时设置了自定义的协议android:scheme意味着可以通过浏览器使用自定义协议打开此activity。可能通过浏览器对app进行越权调用。

fuzz 尽可能多的覆盖到逻辑，
       希望是尽可能测试更底层的代码？

1. 提供种子
2. patch源代码，去掉一些无关紧要的 check，或者提供一个让 fuzzer 能够跑到更底程的专用通道
3. 优化自己的 wrapper，使其测试更多的代码，或者让它测试更底层的代码
    实现将这些字符序列列举出来，fuzz直接使用这些关键字去组合，就可以减少很多没有意义的尝试，同时还有可能会走到更深的程序分支中去。
    Dictionary
  ref https://github.com/rc0r/afl-fuzz/tree/master/dictionaries
4. 自己写 custom mutator，有意识地 fuzz 数据 
5.我要把那两个洞给补了，（快速补法）

当前这个是在fuzz 
DecompressFileW(spInputFilename, spOutputFilename, &nPercentageDone, ProgressCallback, &nKillFlag);

~\Shared\MACLib.h
DLLEXPORT int __stdcall DecompressFileW(const APE::str_utfn * pInputFilename, const APE::str_utfn * pOutputFilename, int * pPercentageDone, APE::APE_PROGRESS_CALLBACK ProgressCallback, int * pKillFlag);
int CAPEHeader::FindDescriptor(bool bSeek) 
CAPEHeader::Analyze  用来分析input的头文件
发现了两个 
1 Win
2 StdLibFileIO.cpp ，maybe第二个
   CStdLibFileIO::Read
这个问题 我用了原始source，等出现了再说
##error 1009 ERROR_INVALID_CHECKSUM
两处
APEDecompress.cpp
APESimple.cpp
### APEDecompress.cpp
### APESimple.cpp
// main decoding loop
        while (nBlocksLeft > 0)
        {
            // decode data。解码数据
            intn nBlocksDecoded = -1; //置-1
            int nResult = spAPEDecompress->GetData((char *) spTempBuffer.GetPtr(), BLOCKS_PER_DECODE, &nBlocksDecoded);
            if (nResult != ERROR_SUCCESS)
                throw(ERROR_INVALID_CHECKSUM);

            // handle the output
            if (nOutputMode == UNMAC_DECODER_OUTPUT_WAV)

CAPEDecompress::FillFrameBuffer 影响Getdata

重新编译之后，error inhere。
    /*********************************************************************************************
    * Decompress / Seek
    *********************************************************************************************/
    
    //////////////////////////////////////////////////////////////////////////////////////////////
    // GetData(...) - gets raw decompressed audio
    //
    // Parameters:
    //    char * pBuffer
    //        a pointer to a buffer to put the data into
    //    int nBlocks
    //        the number of audio blocks desired (see note at intro about blocks vs. samples)
    //    int * pBlocksRetrieved
    //        the number of blocks actually retrieved (could be less at end of file or on critical failure)
    //////////////////////////////////////////////////////////////////////////////////////////////
    virtual int GetData(char * pBuffer, intn nBlocks, intn * pBlocksRetrieved) = 0;

GetData
//有三种，APE、WAV、APEOld

华为音乐无法播放ape文件，

找几百兆的那种，能播放？ 不需要

Huawei music 看看是否还支持ape文件
frida hook住 然后查看 

cat /proc/pid/maps | grep ape

shamu:/data/local/tmp # ps | grep “mediacenter"
USER      PID   PPID  VSIZE  RSS   WCHAN            PC  NAME
u0_a121   18663 11811 1539076 309116 SyS_epoll_ b57bf514 S com.android.mediacenter

1|shamu:/data/local/tmp # cat /proc/18663/maps | grep 'ape'                                                                                                                                               
94845000-9486e000 r-xp 00000000 fe:00 816482     /data/app/com.android.mediacenter-1/lib/arm/libapeplayer.so
9486f000-94870000 r--p 00029000 fe:00 816482     /data/app/com.android.mediacenter-1/lib/arm/libapeplayer.so
94870000-94871000 rw-p 0002a000 fe:00 816482     /data/app/com.android.mediacenter-1/lib/arm/libapeplayer.so

libapeplayer
726FFC1000

64位


APE::CAPETag::LoadField
.text:0001098C                 PUSH    {R4-R7,LR}

64位
17B04C
绝对地址
726BA18B04 

F2 成功断在这个位置，就是为什么没有crash。。。 我得试一试 

华为音乐在运行时支持 ape 文件的解析 ，它使用的是一个第三方的库对ape文件进行解析。该库在处理文件时存在漏洞，可造成进程崩溃造成DoS。与其它漏洞结合可能导致代码执行。

漏洞位于
APE::CAPETag::LoadField  函数中，具体代码及漏洞注释如下：

一共有两个漏洞，一个是整型溢出，导致空指针解引用，进一步导致大片内容任意内容写。
另一个大片是越界读漏洞。





How to debug 
Ref:
http://www.zhongruitech.com/524809042.html
https://blog.csdn.net/nangongyanya/article/details/77992323
https://blog.csdn.net/lwanttowin/article/details/62042095
解析头文件
https://blog.csdn.net/jiangwei0910410003/article/details/50568487
http://download.csdn.net/detail/jiangwei0910410003/9415342