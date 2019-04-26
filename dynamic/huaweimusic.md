# huaweimusic

## 环境
动态环境
关于IDA动态调试步骤，首先你的手机需要ROOT。

1 把ida目录下的android_server文件放到手机的目录，adb pull android_server /data/local/tmp
2 给与android_server 777 权限， chmod 777 android_server
3 端口的转发 adb forward tcp:23946 tcp:23946
4 打开ddms
5 运行android_server ./android_server
6 将要调试的apk文件以调试的方式运行 adb shell am start -D -n com.android.mediacenter/com.android.mediacenter.MainActivity
   包名/.类名
7 这个时候手机显示等到调试连接模式，打开ida，debugger-attach-remote android server 

am start -D -n com.android.mediacenter/.PageActivity

04-25 20:33:25.189: I/ActivityManager(31964): START u0 {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10200000 cmp=com.android.mediacenter/.PageActivity bnds=[237,790][439,1072]} from uid 10024

/data/app/com.android.mediacenter-qR3z1zgFGnBSM2xn3xAchw==/lib/arm64/libapeplayer.so	000000795D304000	0000000000052000

libapeplayer.so	000000796224F000	000000796228E000	R	.	X	D	.	byte	00	public	CODE	64	00	00


## inter
F9,and then F7 F8in

我在libapeplayer基地址处下了断点。但是碰到问题，程序跑不到断点，可能我这里断点下的有问题？。
如何下断点这个问题：

分析一个crash，找到crash的函数，在crash的函数处下断点，尝试。不对，，，，
这里的问题是 运行本crash时，到了这个crash点了么？ 
为什么都没crash：不支持ape（仍然有libapeplayer，可能性低）？问一问

* test 1 
下断点
setDataSource  .text:000000000000F910
libapeplayer 
/data/app/com.android.mediacenter-qR3z1zgFGnBSM2xn3xAchw==/lib/arm64/libapeplayer.so	000000795CC85000	0000000000052000

useless

* test 2 see logcat
两种思路
1 正向
cmp=com.android.mediacenter/.ui.player.MediaPlayBackActivity 下断点

MediaPlayBackActivity$1_init

002292F0
不太好使，总是崩溃

2 反向
分析crash，在哪里crash的下断点

now 分析2个crash，然后动态调试找断点下
暂放一边

* test3 两个思路
《如何定位原因（由外而内）》 ==> 如何定义最外层（找与java直接对应的入口函数） ===> 如何找这些函数（两种方法）
一是 搜 java_xxx_xxx_xxx
二是看 jni_onLoad 函数，在这个函数里面，可能会进行 registerNative 操作
 jniRegisterNativeMethods 函数的定义，看看它的参数是什么意思，然后把它这个东西变成数组，去 correct  一下。
走 第二个思路
jni_onLoad
	__int64 __fastcall JNI_OnLoad(__int64 *a1)
	{
	  __int64 v1; // x4
	  int v2; // w0
	  unsigned int v3; // w1
	  __int64 v5; // [xsp-8h] [xbp-8h]
	  v5 = 0LL;
	  v1 = *a1;
	  qword_516A8 = (__int64)a1;
	  if ( (*(unsigned int (**)(void))(v1 + 48))() )
	  {
	    __android_log_print(6LL, "APE_JNI", "ERROR: GetEnv failed\n");
	    v3 = -1;
	  }
	  else
	  {
	    v2 = jniRegisterNativeMethods(v5, "com/huawei/extendedplayer/ape/APEPlayer", off_51008, 13LL);
	    v3 = 65540;
	    if ( v2 & 0x80000000 )
	    {
	      __android_log_print(6LL, "APE_JNI", "ERROR: MediaPlayer native registration failed\n");
	      v3 = -1;
	    }
	  }
	  return v3;
	}

jniRegisterNativeMethods 函数的定义
RegisterNatives(env, clazz, gMethods, numMethods)

000000796224F000

ta:0000000000051008 off_51008       DCQ aSetdatasource_0    ; DATA XREF: JNI_OnLoad+38↑o
.data:0000000000051008                                         ; JNI_OnLoad+40↑o
.data:0000000000051008                                         ; "_setDataSource"
.data:0000000000051010                 DCQ aLjavaLangStrin_0   ; "(Ljava/lang/String;)V"
.data:0000000000051018                 DCQ sub_E628				000000000000E628 0x796225d628
.data:0000000000051020                 DCQ aPrepareasync_0     ; "_prepareAsync"
.data:0000000000051028                 DCQ aV                  ; "()V"
.data:0000000000051030                 DCQ sub_E594				000000000000E594 0x796225d594
.data:0000000000051038                 DCQ aSeekto_0           ; "_seekTo"
.data:0000000000051040                 DCQ aIV                 ; "(I)V"
.data:0000000000051048                 DCQ sub_E7BC				000000000000E7BC 0x796225d7bc 
.data:0000000000051050                 DCQ aGetcurrentposi     ; "getCurrentPosition"
.data:0000000000051058                 DCQ aI                  ; "()I"
.data:0000000000051060                 DCQ sub_E510				000000000000E510 0x796225d510
.data:0000000000051068                 DCQ aGetduration        ; "getDuration"
.data:0000000000051070                 DCQ aI                  ; "()I"
.data:0000000000051078                 DCQ sub_E48C				000000000000E48C 0x796225d48c
.data:0000000000051080                 DCQ aRelease_0          ; "_release"
.data:0000000000051088                 DCQ aV                  ; "()V"
.data:0000000000051090                 DCQ sub_DEB4				000000000000DEB4 0x796225ceb4
.data:0000000000051098                 DCQ aReset_0            ; "_reset"
.data:00000000000510A0                 DCQ aV                  ; "()V"
.data:00000000000510A8                 DCQ sub_E724				000000000000E728 0x796225d728
.data:00000000000510B0                 DCQ aNativeInit         ; "native_init"
.data:00000000000510B8                 DCQ aV                  ; "()V"
.data:00000000000510C0                 DCQ sub_DF98				DF98	         0x796225cf98
.data:00000000000510C8                 DCQ aNativeSetup        ; "native_setup"
.data:00000000000510D0                 DCQ aLjavaLangObjec_0   ; "(Ljava/lang/Object;)V"
.data:00000000000510D8                 DCQ sub_EA64				EA64             0x796225da64
.data:00000000000510E0                 DCQ aNativeFinalize     ; "native_finalize"
.data:00000000000510E8                 DCQ aV                  ; "()V"
.data:00000000000510F0                 DCQ sub_DF28 							0x796225cf28	
.data:00000000000510F8                 DCQ aGetframe           ; "getFrame"
.data:0000000000051100                 DCQ aLjavaNioBytebu     ; "(Ljava/nio/ByteBuffer;)I"
.data:0000000000051108                 DCQ sub_E3F0 							0x796225d3f0
.data:0000000000051110                 DCQ aGetchannels        ; "getChannels"
.data:0000000000051118                 DCQ aI                  ; "()I"
.data:0000000000051120                 DCQ sub_E350 							0x796225d350
.data:0000000000051128                 DCQ aGetsamplerate      ; "getSampleRate"
.data:0000000000051130                 DCQ aI                  ; "()I"
.data:0000000000051138                 DCQ sub_E2B0 							0x796225d2b0
.data:0000000000051140                 DCQ __gxx_personality_v0
.data:0000000000051148                 ALIGN 0x10
.data:0000000000051150                 EXPORT _ZN3APE7CAPETag18s_aryID3GenreNamesE
