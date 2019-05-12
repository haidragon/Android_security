# 组件-Nextcloud
这个好像是 Nexrcloud 启动之后 
会发出一个upload广播，发送广播以便感兴趣的activity可以更新他们
malware apk 注册如下receiver 可以收到这些广播，可能可以做类似中间人的事情，以至于让其他activity更新为恶意软件
可以拦截有关上传文件的广播
Trigger:与装有Nextcloud的手机上装有malware app，app内静态注册如下receiver
Result: 拦截上传的文件（如果先收到的话）
A malware can simply create a receiver:

'''
<receiver android:exported="true" android:enabled="true" android:name=".InterceptReceiver">
    <intent-filter android:priority="999">
        <action android:name="FileUploader.UPLOAD_START"/>
        <action android:name="FileUploader.UPLOAD_FINISH"/>
        <action android:name="FileUploader.UPLOADS_ADDED"/>
    </intent-filter>
</receiver>
'''

(and other actions)
And receive the broadcasts first than your own receivers

It will disclose info about account, file info, etc

修复
The one thing you should do is to change all calls of Context.sendStickyBroadcast on LocalBroadcastManager.sendBroadcast and all calls of Context.registerReceiver on LocalBroadcastManager.registerReceiver
https://developer.android.com/reference/android/support/v4/content/LocalBroadcastManager.html
instead on using removeStickyBroadcast(intent);

Hi. I believe that using LocalBroadcastManager is the best solution, because it's the easiest one. You have to make less changes to achieve the same result

## extra
启用reciver 通过广播 拦截其他应用上传的文件 ，我猜问题和广播的协议有关
