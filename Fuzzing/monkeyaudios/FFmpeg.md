# FFmpeg
FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。它包括了领先的音/视频编码库libavcodec等。

libavformat：用于各种音视频封装格式的生成和解析，包括获取解码所需信息以生成解码上下文结构
和读取音视频帧等功能；
libavcodec：用于各种类型声音/图像编解码,对信号或者数据流进行变换的程序；
libavutil：包含一些公共的工具函数；
libswscale：用于视频场景比例缩放、色彩映射转换；
libpostproc：用于后期效果处理；
ffmpeg：该项目提供的一个工具，可用于格式转换、解码或电视卡即时编码等；
ffsever：一个 HTTP 多媒体即时广播串流服务器；
ffplay：是一个简单的播放器，使用ffmpeg 库解析和解码，通过SDL显示；

## FFmpeg
参数中文详解
ref https://blog.csdn.net/leixiaohua1020/article/details/12751349
基于FFMPEG的音频编码器
ref https://blog.csdn.net/hy119/article/details/81632662
ref https://baike.baidu.com/item/ffmpeg/2665727?fr=aladdin
* ffmpeg [global_options] {[input_file_options] -i input_url} ... {[output_file_options] output_url} ...
	 _______              ______________
	|       |            |              |
	| input |  demuxer   | encoded data |   decoder
	| file  | ---------> | packets      | -----+
	|_______|            |______________|      |
	                                           v
	                                       _________
	                                      |         |
	                                      | decoded |
	                                      | frames  |
	                                      |_________|
	 ________             ______________       |
	|        |           |              |      |
	| output | <-------- | encoded data | <----+
	| file   |   muxer   | packets      |   encoder
	|________|           |______________|


## libavformat
## libavcodec