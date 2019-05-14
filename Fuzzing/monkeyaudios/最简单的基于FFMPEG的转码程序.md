# 最简单的基于FFMPEG的转码程序
ref 
https://blog.csdn.net/leixiaohua1020/article/details/26838535
本文介绍一个简单的基于FFmpeg的转码器。它可以将一种视频格式（包括封转格式和编码格式）转换为另一种视频格式。转码器在视音频编解码处理的程序中，属于一个比较复杂的东西。因为它结合了视频的解码和编码。一个视频播放器，一般只包含解码功能；一个视频编码工具，一般只包含编码功能；而一个视频转码器，则需要先对视频进行解码，然后再对视频进行编码，因而相当于解码器和编码器的结合。下图例举了一个视频的转码流程。输入视频的封装格式是FLV，视频编码标准是H.264，音频编码标准是AAC；输出视频的封装格式是AVI，视频编码标准是MPEG2，音频编码标准是MP3。从流程中可以看出，首先从输入视频中分离出视频码流和音频压缩码流，然后分别将视频码流和音频码流进行解码，获取到非压缩的像素数据/音频采样数据，接着将非压缩的像素数据/音频采样数据重新进行编码，获得重新编码后的视频码流和音频码流，最后将视频码流和音频码流重新封装成一个文件。

## 流程图
	
	Init -> 
	open_input_file() -> 
	open_output_file() -> 
	init_filters() ->
	av_read_frame() -> 
	AVPacket -> 
	Video? -> 
	Audio? ->
	avcodec_decode_video4()-  > 
	AVFrame -> 
	filter_encode_write_frame() -> 
	flush_encoder() ->
	Quit...

open_input_file()：打开输入文件，并初始化相关的结构体。
open_output_file()：打开输出文件，并初始化相关的结构体。
init_filters()：初始化AVFilter相关的结构体。
av_read_frame()：从输入文件中读取一个AVPacket。
avcodec_decode_video2()：解码一个视频AVPacket（存储H.264等压缩码流数据）为AVFrame（存储YUV等非压缩的像素数据）。
avcodec_decode_video4()：解码一个音频AVPacket（存储MP3等压缩码流数据）为AVFrame（存储PCM采样数据）。
filter_encode_write_frame()：编码一个AVFrame。
flush_encoder()：输入文件读取完毕后，输出编码器中剩余的AVPacket。

* filter_encode_write_frame（）
av_buffersrc_add_frame()->
av_buffersink_get_buffer_ref()->
AVFrame->
Video?->
Audio?->
avcodec_encode_audio2()->
AVPacket->
av_interleaved_write_frame()

简单介绍一下filter_encode_write_frame()中各个函数的意义：

av_buffersrc_add_frame()：将解码后的AVFrame加入Filtergraph。

av_buffersink_get_buffer_ref()：从Filtergraph中取一个AVFrame。

avcodec_encode_video2()：编码一个视频AVFrame为AVPacket。

avcodec_encode_audio2()：编码一个音频AVFrame为AVPacket。

av_interleaved_write_frame()：将编码后的AVPacket写入文件。





