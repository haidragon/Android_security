# 转向ffmeg和chrome以及qq音乐
	ape.c
	https://github.com/FFmpeg/FFmpeg/blob/master/libavformat/ape.c
	ffmpeg的libavformat的ape.c直接使用monkey（看看是否还继续使用）
	有关于ffmeg的bounty（一年没更新了）
	https://hackerone.com/ibb-data
	ffmeg上了hackone
	https://hackerone.com/ffmpeg

	使用FFMPEG作为内核视频播放器：
	Mplayer，ffplay，射手播放器，暴风影音，KMPlayer，QQ影音...

## 下一步
* ffmpeg、qq音乐是否还支持ape，chrome使用了ffmpeg哪些部分
* 分析crash，输出crash报告，fix，继续fuzz

1. qq音乐也有ape，但是不是这个库，但是可能漏洞模式一样。
我还是分析这个库吧先
2. ffmpeg

apetag.c == console.cpp 

ffmpeg
A complete, cross-platform solution to record, convert and stream audio and video.

ffmpeg -i input.mp4 output.avi
我可以验证一下是否可以直接crash
======================
是否可以直接crash
	sudo apt-get install ffmpeg
	test 了 3个 不能直接crash ffmpeg
	说明ffmpeg做了检测
	test 了 fuzz_input里的文件 不能被ffmpeg 解析
	所以接下来 需要改进seeds
======================

改进seeds
======================
下载ape？曾经下载过，没有。如果没有，用其他格式转成ape
小一点，3个就够了
小一点 随便的，以及大的
重新编译./mac 重新进行fuzz 进行尝试
就边看边审计，看看每一个输入能够控制到的变量
是否在fuzz过程中，都达到过它们的边界值
如果达到边界值，会产生什么后果

种子质量问题
就是尽可能让种子差异化大不同的参数，不同的transformer，不同的源文件格式去进行转换，就可以得到 varieties of seeds
熟悉一波ffmpeg
控制输入
下载pcm mp3 avi wav格式
转换成ape格式
https://www.poweriso.com/tutorials/convert-to-ape.htm
======================



# 联系方式
	https://monkeysaudio.com/contact.html
	mail@monkeysaudio.com