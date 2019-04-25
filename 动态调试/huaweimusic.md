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


04-25 20:33:25.189: I/ActivityManager(31964): START u0 {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10200000 cmp=com.android.mediacenter/.PageActivity bnds=[237,790][439,1072]} from uid 10024

