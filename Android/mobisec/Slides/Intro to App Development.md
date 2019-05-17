# Intro to App Development
ref:https://docs.google.com/presentation/d/1cqiHIosidNXZTT7GiRmfz86JbCCuKrK14OwnvDUOZyA/edit#slide=id.g4368a15dfb_0_27
* how an Android app looks like
* how to develop them
* hoe to run them
* DEMO on all tree steps
* Website walkthrough

1. Example of APIs: HTTP request

URL url = new URL("http://www.android.com/");
HttpURLConnection urlConnection = (HttpURLConnection)
url.openConnection();
try{
	InputStream in = new BufferedInputStream(urlConnection.getInputStream());
	readStream(in);
}finally{
	urlConnection.disconnect();
}

Log.i("MYAPP","Logging a message");
Log.e("MOBISEC","Test message");