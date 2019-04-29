# huawei-music-crash-3

* 环境

	root@9b798cc2ff72:/tmp/tool/MAC_SDK_448# pwd
	/tmp/tool/MAC_SDK_448
	root@9b798cc2ff72:/tmp/tool/MAC_SDK_448# export  LD_LIBRARY_PATH=.

	crash 10 

	corrupted size vs. prev_size: xxxxxxxxxx    内存溢出
	memcpy() , memset() 等函数执行时给定的长度，即字节数 过长造成的溢出.
* 结果

	root@9b798cc2ff72:/tmp/tool/MAC_SDK_448# ./mac ./fuzz_out/crashes/id\:000010\,sig\:06\,src\:000000\,op\:havoc\,rep\:8 test.wav -d
	--- Monkey's Audio Console Front End (v 4.48) (c) Matthew T. Ashland ---

	 argv[1] : ./fuzz_out/crashes/id:000010,sig:06,src:000000,op:havoc,rep:8

	size : 108
	Decompressing...
	*** Error in './mac': corrupted size vs. prev_size: 0x0000000001b7c220 ***            
	======= Backtrace: =========
	/lib/x86_64-linux-gnu/libc.so.6(+0x777e5)[0x7faa5a9877e5]
	/lib/x86_64-linux-gnu/libc.so.6(+0x80dfb)[0x7faa5a990dfb]
	/lib/x86_64-linux-gnu/libc.so.6(cfree+0x4c)[0x7faa5a99453c]
	./libMAC.so.4(_ZN3APE18CAPEDecompressCoreD1Ev+0x16e)[0x7faa5b2acb34]
	./libMAC.so.4(_ZN3APE6CUnMAC12UninitializeEv+0x3a)[0x7faa5b2af668]
	./libMAC.so.4(_ZN3APE6CUnMACD1Ev+0x18)[0x7faa5b2af508]
	./libMAC.so.4(_ZN3APE17CAPEDecompressOldD1Ev+0x41)[0x7faa5b2ada7b]
	./libMAC.so.4(_ZN3APE17CAPEDecompressOldD0Ev+0x18)[0x7faa5b2adb12]
	./libMAC.so.4(_ZN3APE9CSmartPtrINS_14IAPEDecompressEE6DeleteEv+0xbd)[0x7faa5b296b2f]
	./libMAC.so.4(_Z14DecompressCorePKwS0_iiPN3APE20IAPEProgressCallbackE+0x1077)[0x7faa5b2963af]
	./libMAC.so.4(DecompressFileW2+0x56)[0x7faa5b2952fc]
	./libMAC.so.4(DecompressFileW+0x5b)[0x7faa5b29421b]
	./mac[0x4048dc]
	/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0)[0x7faa5a930830]
	./mac[0x402579]
	======= Memory map: ========
	00400000-00406000 r-xp 00000000 08:02 1042173                            /tmp/tool/MAC_SDK_448/mac
	00605000-00606000 r--p 00005000 08:02 1042173                            /tmp/tool/MAC_SDK_448/mac
	00606000-00607000 rw-p 00006000 08:02 1042173                            /tmp/tool/MAC_SDK_448/mac
	00607000-00609000 rw-p 00000000 00:00 0 
	01b3b000-01bb8000 rw-p 00000000 00:00 0                                  [heap]
	7faa54000000-7faa54021000 rw-p 00000000 00:00 0 
	7faa54021000-7faa58000000 ---p 00000000 00:00 0 
	7faa5a607000-7faa5a70f000 r-xp 00000000 08:02 809426                     /lib/x86_64-linux-gnu/libm-2.23.so
	7faa5a70f000-7faa5a90e000 ---p 00108000 08:02 809426                     /lib/x86_64-linux-gnu/libm-2.23.so
	7faa5a90e000-7faa5a90f000 r--p 00107000 08:02 809426                     /lib/x86_64-linux-gnu/libm-2.23.so
	7faa5a90f000-7faa5a910000 rw-p 00108000 08:02 809426                     /lib/x86_64-linux-gnu/libm-2.23.so
	7faa5a910000-7faa5aad0000 r-xp 00000000 08:02 809413                     /lib/x86_64-linux-gnu/libc-2.23.so
	7faa5aad0000-7faa5acd0000 ---p 001c0000 08:02 809413                     /lib/x86_64-linux-gnu/libc-2.23.so
	7faa5acd0000-7faa5acd4000 r--p 001c0000 08:02 809413                     /lib/x86_64-linux-gnu/libc-2.23.so
	7faa5acd4000-7faa5acd6000 rw-p 001c4000 08:02 809413                     /lib/x86_64-linux-gnu/libc-2.23.so
	7faa5acd6000-7faa5acda000 rw-p 00000000 00:00 0 
	7faa5acda000-7faa5acf0000 r-xp 00000000 08:02 804954                     /lib/x86_64-linux-gnu/libgcc_s.so.1
	7faa5acf0000-7faa5aeef000 ---p 00016000 08:02 804954                     /lib/x86_64-linux-gnu/libgcc_s.so.1
	7faa5aeef000-7faa5aef0000 rw-p 00015000 08:02 804954                     /lib/x86_64-linux-gnu/libgcc_s.so.1
	7faa5aef0000-7faa5b062000 r-xp 00000000 08:02 805767                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
	7faa5b062000-7faa5b262000 ---p 00172000 08:02 805767                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
	7faa5b262000-7faa5b26c000 r--p 00172000 08:02 805767                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
	7faa5b26c000-7faa5b26e000 rw-p 0017c000 08:02 805767                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
	7faa5b26e000-7faa5b272000 rw-p 00000000 00:00 0 
	7faa5b272000-7faa5b2bb000 r-xp 00000000 08:02 1042161                    /tmp/tool/MAC_SDK_448/libMAC.so.4
	7faa5b2bb000-7faa5b4bb000 ---p 00049000 08:02 1042161                    /tmp/tool/MAC_SDK_448/libMAC.so.4
	7faa5b4bb000-7faa5b4bc000 r--p 00049000 08:02 1042161                    /tmp/tool/MAC_SDK_448/libMAC.so.4
	7faa5b4bc000-7faa5b4be000 rw-p 0004a000 08:02 1042161                    /tmp/tool/MAC_SDK_448/libMAC.so.4
	7faa5b4be000-7faa5b4c0000 rw-p 00000000 00:00 0 
	7faa5b4c0000-7faa5b4e6000 r-xp 00000000 08:02 809406                     /lib/x86_64-linux-gnu/ld-2.23.so
	7faa5b6da000-7faa5b6df000 rw-p 00000000 00:00 0 
	7faa5b6e3000-7faa5b6e5000 rw-p 00000000 00:00 0 
	7faa5b6e5000-7faa5b6e6000 r--p 00025000 08:02 809406                     /lib/x86_64-linux-gnu/ld-2.23.so
	7faa5b6e6000-7faa5b6e7000 rw-p 00026000 08:02 809406                     /lib/x86_64-linux-gnu/ld-2.23.so
	7faa5b6e7000-7faa5b6e8000 rw-p 00000000 00:00 0 
	7ffe09c32000-7ffe09c53000 rw-p 00000000 00:00 0                          [stack]
	7ffe09d1a000-7ffe09d1d000 r--p 00000000 00:00 0                          [vvar]
	7ffe09d1d000-7ffe09d1f000 r-xp 00000000 00:00 0                          [vdso]
	ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
	Aborted (core dumped)

* 调试
	gdb-peda$ set args ./fuzz_out/crashes/id\:000010\,sig\:06\,src\:000000\,op\:havoc\,rep\:8 test.wav -d
	gdb-peda$ b main 
	Breakpoint 1 at 0x408d7e: file Source/Console/Console.cpp, line 126.
	gdb-peda$ run
	gdb-peda$ c

Stopped reason: SIGABRT
0x00007ffff725c428 in __GI_raise (sig=sig@entry=0x6) at ../sysdeps/unix/sysv/linux/raise.c:54
54	../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
gdb-peda$ l
49	in ../sysdeps/unix/sysv/linux/raise.c


#0  0x00007ffff725c428 in __GI_raise (sig=sig@entry=0x6) at ../sysdeps/unix/sysv/linux/raise.c:54
#1  0x00007ffff725e02a in __GI_abort () at abort.c:89
#2  0x00007ffff729e7ea in __libc_message (do_abort=0x2, fmt=fmt@entry=0x7ffff73b7ed8 "*** Error in `%s': %s: 0x%s ***\n")
    at ../sysdeps/posix/libc_fatal.c:175
#3  0x00007ffff72a7dfb in malloc_printerr (ar_ptr=0x7ffff75ebb20 <main_arena>, ptr=0x64a220, 
    str=0x7ffff73b4c75 "corrupted size vs. prev_size", action=0x3) at malloc.c:5006
#4  _int_free (av=0x7ffff75ebb20 <main_arena>, p=<optimized out>, have_lock=0x0) at malloc.c:4014
#5  0x00007ffff72ab53c in  (mem=<optimized out>) at malloc.c:2968
#6  0x00007ffff7bc3b34 in APE::CAPEDecompressCore::~CAPEDecompressCore (this=0x62f090, __in_chrg=<optimized out>)
    at Source/MACLib/Old/APEDecompressCore.cpp:49
#7  0x00007ffff7bc6668 in APE::CUnMAC::Uninitialize (this=0x620d20) at Source/MACLib/Old/UnMAC.cpp:96
#8  0x00007ffff7bc6508 in APE::CUnMAC::~CUnMAC (this=0x620d20, __in_chrg=<optimized out>)
    at Source/MACLib/Old/UnMAC.cpp:53
#9  0x00007ffff7bc4a7b in APE::CAPEDecompressOld::~CAPEDecompressOld (this=0x620cd0, __in_chrg=<optimized out>)
    at Source/MACLib/Old/APEDecompressOld.cpp:46
#10 0x00007ffff7bc4b12 in APE::CAPEDecompressOld::~CAPEDecompressOld (this=0x620cd0, __in_chrg=<optimized out>)
    at Source/MACLib/Old/APEDecompressOld.cpp:49
#11 0x00007ffff7badb2f in APE::CSmartPtr<APE::IAPEDecompress>::Delete (this=0x7fffffffe390) at Source/Shared/SmartPtr.h:56
#12 0x00007ffff7bad3af in DecompressCore (pInputFilename=0x61b030 L"tempfile.ape", 
    pOutputFilename=0x61b070 L"tempoutputfl", nOutputMode=0x1, nCompressionLevel=0xffffffff, 
    pProgressCallback=0x7fffffffe480) at Source/MACLib/APESimple.cpp:489
#13 0x00007ffff7bac2fc in DecompressFileW2 (pInputFilename=0x61b030 L"tempfile.ape", 
    pOutputFilename=0x61b070 L"tempoutputfl", pProgressCallback=0x7fffffffe480) at Source/MACLib/APESimple.cpp:322
#14 0x00007ffff7bab21b in DecompressFileW (pInputFilename=0x61b030 L"tempfile.ape", 
    pOutputFilename=0x61b070 L"tempoutputfl", pPercentageDone=0x7fffffffe4ec, 
    ProgressCallback=0x40450e <ProgressCallback(int)>, pKillFlag=0x7fffffffe4f0) at Source/MACLib/APESimple.cpp:102
#15 0x00000000004048dc in main (argc=0x4, argv=0x7fffffffe6d8) at Source/Console/Console.cpp:262
#16 0x00007ffff7247830 in __libc_start_main (main=0x40463c <main(int, char**)>, argc=0x4, argv=0x7fffffffe6d8, 
    init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffe6c8)
    at ../csu/libc-start.c:291
#17 0x0000000000402579 in _start ()

/*****************************************************************************************
Uninitialize
*****************************************************************************************/
int CUnMAC::Uninitialize() 
{
    if (m_bInitialized) 
    {
        SAFE_DELETE(m_pAPEDecompressCore)
        SAFE_DELETE(m_pPrepare)
        
        // clear the APE info pointer
        m_pAPEDecompress = NULL;

        // set the last decoded frame again
        m_LastDecodedFrameIndex = -1;

        // set the initialized flag to false
        m_bInitialized = false;
    }

    return ERROR_SUCCESS;
}

对于没有初始化的进行初始化，SAFE_DELETE的时候发生了错误

 if (m_bInitialized)  

gdb-peda$ p m_bInitialized
$1 = 0x1 
说明未初始化

程序主动 abort 或者是 assert 导致的 crash

