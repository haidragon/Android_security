huawei-music-crash-2

0x01 结果

root@9b798cc2ff72:/tmp/tool/MAC_SDK_448# ./mac ./fuzz_out/crashes/id\:000001\,sig\:11\,src\:000000\,op\:flip1\,pos\:5 test.wav -d

--- Monkey's Audio Console Front End (v 4.48) (c) Matthew T. Ashland ---

 argv[1] : ./fuzz_out/crashes/id:000001,sig:11,src:000000,op:flip1,pos:5 //此处为编译Mac时 自写插入

size : 128
Decompressing...
Segmentation fault (core dumped)

0x02 调试

root@9b798cc2ff72:/tmp/tool/MAC_SDK_448# gdb ./mac 

gdb-peda$ set args ./fuzz_out/crashes/id\:000001\,sig\:11\,src\:000000\,op\:flip1\,pos\:5 test.wav -d
gdb-peda$ b main 
Breakpoint 1 at 0x408d7e: file Source/Console/Console.cpp, line 126.
gdb-peda$ run
gdb-peda$ c
[----------------------------------registers-----------------------------------]
RAX: 0x7ffff7ff1000 
RBX: 0x40 ('@')
RCX: 0x22ff80 
RDX: 0x7ffff7fab010 --> 0x0 
RSI: 0x0 
RDI: 0x62f0e0 --> 0x7ffff7dd2c08 --> 0x7ffff7bc596a (<APE::CUnBitArrayOld::~CUnBitArrayOld()>:  push   rbp)
RBP: 0x7fffffffdd60 --> 0x7fffffffdd90 --> 0x7fffffffe000 --> 0x7fffffffe050 --> 0x7fffffffe0d0 --> 0x7fffffffe100 (--> ...)
RSP: 0x7fffffffdce0 --> 0x73c 
RIP: 0x7ffff7bc5e54 (<APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+756>:      mov    esi,DWORD PTR [rax])
R8 : 0x61f2c0 --> 0x0 
R9 : 0x61f1e0 --> 0xfbad2480 
R10: 0x32b 
R11: 0x7ffff7bc61e4 (<APE::CUnBitArrayOld::Get_K(unsigned int)>:        push   rbp)
R12: 0x7ffff7bc4c38 (<APE::CAPEDecompressOld::GetData(char*, long long, long long*)>:   push   rbp)
R13: 0x2c (',')
R14: 0x0 
R15: 0x0
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x7ffff7bc5e4b <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+747>: mov    eax,eax
   0x7ffff7bc5e4d <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+749>: shl    rax,0x2
   0x7ffff7bc5e51 <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+753>: add    rax,rdx
=> 0x7ffff7bc5e54 <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+756>: mov    esi,DWORD PTR [rax]
   0x7ffff7bc5e56 <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+758>: mov    rax,QWORD PTR [rbp-0x68]
   0x7ffff7bc5e5a <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+762>: mov    eax,DWORD PTR [rax+0x30]
   0x7ffff7bc5e5d <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+765>: lea    ecx,[rax+0x1]
   0x7ffff7bc5e60 <APE::CUnBitArrayOld::GenerateArrayOld(int*, unsigned int, int)+768>: mov    rdx,QWORD PTR [rbp-0x68]
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdce0 --> 0x73c 
0008| 0x7fffffffdce8 --> 0x240000027dd0 
0016| 0x7fffffffdcf0 --> 0x6411e0 --> 0xc0feeab13f017400 
0024| 0x7fffffffdcf8 --> 0x62f0e0 --> 0x7ffff7dd2c08 --> 0x7ffff7bc596a (<APE::CUnBitArrayOld::~CUnBitArrayOld()>:      push   rbp)
0032| 0x7fffffffdd00 --> 0x600000001 
0040| 0x7fffffffdd08 --> 0x6691dcff0062f0e0 
0048| 0x7fffffffdd10 --> 0x40 ('@')
0056| 0x7fffffffdd18 --> 0x80ffffffff 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00007ffff7bc5e54 in APE::CUnBitArrayOld::GenerateArrayOld (this=0x62f0e0, Output_Array=0x6411e0, Number_of_Elements=0x2400, Minimum_nCurrentBitIndex_Array_Bytes=0x27dd0)
    at Source/MACLib/Old/UnBitArrayOld.cpp:196
196             while (!(m_pBitArray[m_nCurrentBitIndex >> 5] & Powers_of_Two_Reversed[m_nCurrentBitIndex++ & 31])) {}
碰到一个坑，AFL 插桩 导致value optimized！ 用普通的clang编译就行


gdb-peda$ bt
#0  0x00007ffff7bc5e54 in APE::CUnBitArrayOld::GenerateArrayOld (this=0x62f0e0, Output_Array=0x6411e0,
    Number_of_Elements=0x2400, Minimum_nCurrentBitIndex_Array_Bytes=0x27dd0) at Source/MACLib/Old/UnBitArrayOld.cpp:196
#1  0x00007ffff7bc60f6 in APE::CUnBitArrayOld::GenerateArray (this=0x62f0e0, pOutputArray=0x6411e0, nElements=0x2400,
    nBytesRequired=0x27dd0) at Source/MACLib/Old/UnBitArrayOld.cpp:250
#2  0x00007ffff7bc417c in APE::CAPEDecompressCore::GenerateDecodedArray (this=0x62f090, Input_Array=0x62f140,
    Number_of_Elements=0x2400, Frame_Index=0x0, pAntiPredictor=0x624df0, CPULoadBalancingFactor=0x0)
    at Source/MACLib/Old/APEDecompressCore.cpp:148
#3  0x00007ffff7bc3ca0 in APE::CAPEDecompressCore::GenerateDecodedArrays (this=0x62f090, nBlocks=0x2400,
    nSpecialCodes=0x0, nFrameIndex=0x0, nCPULoadBalancingFactor=0x0) at Source/MACLib/Old/APEDecompressCore.cpp:70
#4  0x00007ffff7bc6c25 in APE::CUnMAC::DecompressFrameOld (this=0x620d20, pOutputData=0x65c260 "", FrameIndex=0x0,
    CPULoadBalancingFactor=0x0) at Source/MACLib/Old/UnMAC.cpp:200
#5  0x00007ffff7bc66fc in APE::CUnMAC::DecompressFrame (this=0x620d20, pOutputData=0x65c260 "", FrameIndex=0x0,
    CPULoadBalancingFactor=0x0) at Source/MACLib/Old/UnMAC.cpp:117
#6  0x00007ffff7bc5047 in APE::CAPEDecompressOld::Seek (this=0x620cd0, nBlockOffset=0x0)
    at Source/MACLib/Old/APEDecompressOld.cpp:157
#7  0x00007ffff7bc4c30 in APE::CAPEDecompressOld::InitializeDecompressor (this=0x620cd0)
    at Source/MACLib/Old/APEDecompressOld.cpp:70
#8  0x00007ffff7bc4c71 in APE::CAPEDecompressOld::GetData (this=0x620cd0, pBuffer=0x626050 "", nBlocks=0x2400,
    pBlocksRetrieved=0x7fffffffe2b0) at Source/MACLib/Old/APEDecompressOld.cpp:77
#9  0x00007ffff7bacac0 in DecompressCore (pInputFilename=0x61b030 L"tempfile.ape",
    pOutputFilename=0x61b070 L"tempoutputfl", nOutputMode=0x1, nCompressionLevel=0xffffffff,
    pProgressCallback=0x7fffffffe430) at Source/MACLib/APESimple.cpp:406
#10 0x00007ffff7bac2fc in DecompressFileW2 (pInputFilename=0x61b030 L"tempfile.ape",
    pOutputFilename=0x61b070 L"tempoutputfl", pProgressCallback=0x7fffffffe430) at Source/MACLib/APESimple.cpp:322
#11 0x00007ffff7bab21b in DecompressFileW (pInputFilename=0x61b030 L"tempfile.ape",
    pOutputFilename=0x61b070 L"tempoutputfl", pPercentageDone=0x7fffffffe49c,
    ProgressCallback=0x40450e <ProgressCallback(int)>, pKillFlag=0x7fffffffe4a0) at Source/MACLib/APESimple.cpp:102
#12 0x00000000004048dc in main (argc=0x4, argv=0x7fffffffe688) at Source/Console/Console.cpp:262
#13 0x00007ffff7247830 in __libc_start_main (main=0x40463c <main(int, char**)>, argc=0x4, argv=0x7fffffffe688,
    init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffe678)
    at ../csu/libc-start.c:291
#14 0x0000000000402579 in _start ()

查看源代码
196             while (!(m_pBitArray[m_nCurrentBitIndex >> 5] & Powers_of_Two_Reversed[m_nCurrentBitIndex++ & 31])) {}
我猜 数组下标越界访问 
经分析
m_pBitArray 
gdb-peda$ p m_nCurrentBitIndex
$21 = 0x22ff80
gdb-peda$ p m_nCurrentBitIndex >> 5
$22 = 0x117fc
转为int为 m_nCurrentBitIndex = 71676
Xref 
/Users/miy1z1ki/Desktop/huawei_music_git/MAC_SDK_448/Source/MACLib/BitArray.cpp:
   14#define BIT_ARRAY_ELEMENTS            (4096)                        // the number of elements in the bit array (4 MB)
   ...
   48  {
   49      // allocate memory for the bit array
   50:     m_pBitArray = new uint32 [BIT_ARRAY_ELEMENTS];
   ...

m_nCurrentBitIndex 怎么传过来的呢
我想watch m_nCurrentBitIndex 
q=0时，正常
q=1时，m_nCurrentBitIndex = 0x208726
Source/MACLib/Old/UnBitArrayOld.cpp

    //m_nCurrentBitIndex = 0x3c

148         // decode the first 5 elements (all k = 10)
149         Max = (Number_of_Elements < 5) ? Number_of_Elements : 5;
150         for (q = 0; q < Max; q++) 
151         {
152             Output_Array[q] = DecodeValueRiceUnsigned(10);
153         }
154         
    //m_nCurrentBitIndex = 0x208726
gdb watch 全局变量或当前堆栈区可见变量才能watch
Source/MACLib/Old/UnBitArrayOld.cpp

uint32 CUnBitArrayOld::DecodeValueRiceUnsigned(uint32 k) 
{
    // variable declares
    uint32 v;
    
    // plug through the string of 0's (the overflow)
    uint32 BitInitial = m_nCurrentBitIndex;
    while (!(m_pBitArray[m_nCurrentBitIndex >> 5] & Powers_of_Two_Reversed[m_nCurrentBitIndex++ & 31])) {}
    
    // if k = 0, your done
    if (k == 0)
        return (m_nCurrentBitIndex - BitInitial - 1);
    
    // put the overflow value into v
    v = (m_nCurrentBitIndex - BitInitial - 1) << k;
    
    return v | DecodeValueXBits(k);

m_pBitArray 一直为 0 导致 
while (!(m_pBitArray[m_nCurrentBitIndex >> 5] & Powers_of_Two_Reversed[m_nCurrentBitIndex++ & 31])) {}
一直过不去，直到访问的内存不可读写 报错  //可以patch 限制 长度。

m_pBitArray 为什么一直为0. m_pBitArray哪来的

