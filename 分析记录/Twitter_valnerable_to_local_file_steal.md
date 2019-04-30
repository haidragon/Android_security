# Twitter lite(Android): Vulnerable to local file steal, Javascript injection, Open redirect
com.twitter.android.lite.TwitterLiteActivity 导出，
不会验证数据传递给intent，因为此活动容易窃取用户本地文件，javascript注入和打开重定向。
说明：com.twitter.android.lite.TwitterLiteActivity设置为导出，以便外部应用程序可以与之通信。
由于此活动不验证数据通过意图关键uri如javascript和文件，因此恶意应用程序可以窃取用户文件以及注入javascript。
它可能导致许多问题，如UXSS，Token窃取等。
ref https://hackerone.com/reports/499348
