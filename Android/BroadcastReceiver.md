# BroadcastReceiver
## 基本概念
BroadcastReceiver就是应用程序间的全局大喇叭，即通信的一个手段， 系统自己在很多时候都会发送广播，程序就只会接收到自己所关心的广播内容,这些广播可能来自于系统,也可能来自于其他应用程序。比如电量低或者充足，刚启动完，插入耳机，输入法改变等， 发生这些事件，系统都会发送广播，这个叫系统广播，每个APP都会收到，如果你想让你的应用在接收到 这个广播的时候做一些操作，比如：系统开机后，偷偷后台跑服务，这个时候你只需要为你的应用 注册一个用于监视开机的BroadcastReceiver。

## 广播的使用实例
### 动态注册监听网络变化
广播的动态注册就是在java代码中指定IntentFilter，然后添加不同的Action即可，想监听什么广播就写什么Action，另外动态注册的广播，一定要调用unregisterReceiver()这个方法，让广播取消注册。

'''java
	package com.nyl.broadcasttest;
	import android.app.Activity;
	import android.content.BroadcastReceiver;
	import android.content.Context;
	import android.content.Intent;
	import android.content.IntentFilter;
	import android.support.v7.app.AppCompatActivity;
	import android.os.Bundle;
	import android.widget.Toast;
	public class MainActivity extends Activity {
	    private IntentFilter intentFilter;
	    private NetworkChangeReceiver networkChangeReceiver;
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_main);
	        //创建IntentFilter的实例
	        intentFilter = new IntentFilter();
	        /**
	         * 当网络状态发生变化时,系统发出的正是一条值为android.net.conn.CONNECTIVITY_CHANGE的广播
	         * 也就是我们广播接收器想要监听什么广播，在这里添加相对应的Action就行了
	         */
	        intentFilter.addAction("android.net.conn.CONNECTIVITY_CHANGE");
	        /**
	         * 实例化NetworkChangeReceiver的实例和IntentFilter的实例都传了进去,
	         * NetworkChangeReceiver就会收到所有值为android.net.conn.CONNECTIVITY_CHANGE的广播，
	         * 也就实现了监听网络变化的功能
	         */
	        networkChangeReceiver = new NetworkChangeReceiver();
	        registerReceiver(networkChangeReceiver,intentFilter);
	    }
	    /**
	     * 动态注册的广播接收器一定都要取消注册才行,这里是在onDestroy()方法中通过调用
	     * unregisterReceiver()方法来实现的
	     */
	    @Override
	    protected void onDestroy() {
	        super.onDestroy();
	        unregisterReceiver(networkChangeReceiver);
	    }
	    //定义一个广播，继承自BroadcastReceiver
	    private class NetworkChangeReceiver extends BroadcastReceiver{
	        /**
	         * 重写了父类的onReceive()方法，
	         * 每当网络请求发生变化时,onReceive()方法就会得到执行
	         * @param context
	         * @param intent
	         */
	        @Override
	        public void onReceive(Context context, Intent intent) {
	            Toast.makeText(context,"没有网络,请连接网络!",Toast.LENGTH_SHORT).show();
	        }
	    }
	}
'''

### 静态注册实现开机启动
动态注册需程序启动后才能接受到广播，静态广播就弥补了这个短板，在AndroidManifest.xml中制定<IntentReceiver>就可以让程序在未启动的情况下接受到了广播。
程序接收一条开机广播,当收到这个广播时就可以在onReceive()方法里执行相应的逻辑，从而实现开机启动的功能。代码如下：
'''java
	package com.nyl.broadcasttest;
	import android.content.BroadcastReceiver;
	import android.content.Context;
	import android.content.Intent;
	import android.widget.Toast;
	public class BootCompleteReceiver extends BroadcastReceiver{
	    private final String ACTION_BOOT = "android.intent.action.BOOT_COMPLETED";
	    @Override
	    public void onReceive(Context context, Intent intent) {
	        if (ACTION_BOOT.equals(intent.getAction())){
	            Toast.makeText(context,"开机完毕",Toast.LENGTH_SHORT).show();
	        }
	    }
	}
'''

在AndroidManifest.xml中对该BroadcastReceiver进行注册，添加开机广播的intent-filter!对了，别忘了加上android.permission.RECEIVE_BOOT_COMPLETED的权限哦

## Android 之使用LocalBroadcastManager解决BroadcastReceiver安全问题
在Android系统中,BroadcastReceiver的设计初衷就是从全局考虑的，可以方便应用程序和系统、应用程序之间、应用程序内的通信，所以对单个应用程序而言BroadcastReceiver是存在安全性问题的，相应问题及解决如下：

1.  当应用程序发送某个广播时系统会将发送的Intent与系统中所有注册的BroadcastReceiver的IntentFilter进行匹配，若匹配成功则执行相应的onReceive函数。可以通过类似sendBroadcast(Intent, String)的接口在发送广播时指定接收者必须具备的permission。或通过Intent.setPackage设置广播仅对某个程序有效。

2.  当应用程序注册了某个广播时，即便设置了IntentFilter还是会接收到来自其他应用程序的广播进行匹配判断。对于动态注册的广播可以通过类似registerReceiver(BroadcastReceiver, IntentFilter, String, android.os.Handler)的接口指定发送者必须具备的permission，对于静态注册的广播可以通过android:exported="false"属性表示接收者对外部应用程序不可用，即不接受来自外部的广播。

上面两个问题其实都可以通过LocalBroadcastManager来解决:

Android v4 兼容包提供android.support.v4.content.LocalBroadcastManager工具类，帮助大家在自己的进程内进行局部广播发送与注册，使用它比直接通过sendBroadcast(Intent)发送系统全局广播有以下几点好处。

1.   因广播数据在本应用范围内传播，你不用担心隐私数据泄露的问题。

2.   不用担心别的应用伪造广播，造成安全隐患。

3    相比在系统内发送全局广播，它更高效。