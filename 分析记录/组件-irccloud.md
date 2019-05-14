# irccloud
盗窃任意受保护的文件

com.irccloud.android.activity.ShareChooserActivity被导出，并设计为允许从第三方应用程序共享文件到IRC Cloud。

'''html
	<activity android:excludeFromRecents="true" android:name="com.irccloud.android.activity.ShareChooserActivity" android:theme="@style/dawnDialog">
            <intent-filter>
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.DEFAULT"/>
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.SEND"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <data android:mimeType="application/*"/>
                <data android:mimeType="audio/*"/>
                <data android:mimeType="image/*"/>
                <data android:mimeType="text/*"/>
                <data android:mimeType="video/*"/>
            </intent-filter>
            <meta-data android:name="android.service.chooser.chooser_target_service" android:value=".ConversationChooserTargetService"/>
        </activity>
'''


'''java
	protected void onResume() {
        //...
        if (getSharedPreferences("prefs", 0).getString("session_key", "").length() > 0) {
                //...
                this.mUri = (Uri) getIntent().getParcelableExtra("android.intent.extra.STREAM"); // getting attacker provided uri
                if (this.mUri != null) {
                    this.mUri = MainActivity.makeTempCopy(this.mUri, this); // copying file from this uri to /data/data/com.irccloud.android/cache/
                }
'''

'''java
	public static Uri makeTempCopy(Uri fileUri, Context context, String original_filename) { // original_filename = mUri.getLastPathSegment()
        //...
        try {
            Uri out = Uri.fromFile(new File(context.getCacheDir(), original_filename));
            Log.d("IRCCloud", "Copying file to " + out);
            InputStream is = IRCCloudApplication.getInstance().getApplicationContext().getContentResolver().openInputStream(fileUri);
            OutputStream os = IRCCloudApplication.getInstance().getApplicationContext().getContentResolver().openOutputStream(out);
            byte[] buffer = new byte[8192];
            while (true) {
                int len = is.read(buffer);
                if (len != -1) {
                    os.write(buffer, 0, len);
                //...
'''


# [IRCCloud Android] Opening arbitrary URLs/XSS in SAMLAuthActivity
com.irccloud.android.activity.SAMLAuthActivity隐式导出，
'''
if (getIntent() == null || !getIntent().hasExtra("auth_url")) {
    finish();
    return;
}
getSupportActionBar().setTitle(getIntent().getStringExtra("title"));
this.mWebView.loadUrl(getIntent().getStringExtra("auth_url"));
'''