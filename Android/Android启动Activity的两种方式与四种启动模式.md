# Android启动Activity的两种方式与四种启动模式
## 在一个Activity 调用 startActivity()
## 在一个Activity 调用 startActivityRequest()
重写onActivityResult方法，接受B回传的数据。在B中回传数据时采用setResult方法，并且之后要调用finish方法。
第一种方法简单直接。但是如果A调用B，并传递数据，同时B对数据处理后又返回给A，A再将数据显示出来。碰到这种情况，用第一种方法需要在A的onCreate()里面判断是第一次生成的界面，还是由B打开的A。这样比较麻烦，用第二种方法就简单了，在A的onCreate()只用写一次生成的界面的内容。在A的onActivityResult方法里放B处理完数据后的内容就可以了。
'''
	Intent intent = new Intent(MainActivity.this, ActivityA.class);
    startActivity(intent);
    Intent intent = new Intent(MainActivity.this, ActivityB.class);
    startActivityForResult(intent, RequestCodeB);
    Intent intent = new Intent(MainActivity.this, ActivityC.class);
    startActivityForResult(intent, RequestCodeC);
    /********************************************************************************
     * Activity回调
     *******************************************************************************/
    public static final int RequestCodeA = 10001;
    public static final int RequestCodeB = 10002;
    public static final int RequestCodeC = 10003;
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == RequestCodeA && resultCode == RESULT_OK) {
            Log.d("MainActivity", "onActivityResultA");
        } else if (requestCode == RequestCodeB && resultCode == RESULT_OK) {
            Log.d("MainActivity", "onActivityResultB");
        } else if (requestCode == RequestCodeC && resultCode == RESULT_OK) {
            String string=data.getStringExtra("data");
            Log.d("MainActivity", "onActivityResultC:"+string);
        }
    };
'''

--------------

## Activity启动方式 四种

* standard

* singleTop

* singleTask

* singleInstance

设置Activity的启动模式，只需要在AndroidManifest.xml里对应的<activity>标签设置android:launchMode属性，例如：
	'''
	<activity  
    android:name=".A1"  
    android:launchMode="standard" />  
	'''


