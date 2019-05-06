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

## 源码编译ffmpeg
* 根据此来编译http://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg

* 下载依赖
apt-get update -qq && apt-get -y install autoconf automake build-essential cmake git-core libass-dev libfreetype6-dev libsdl2-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo wget zlib1g-dev

中间有一段失了智一般的安装操作
===========

git -C x264 pull 2> /dev/null || git clone --depth 1 https://code.videolan.org/videolan/x264.git && \
cd x264 && \
PKG_CONFIG_PATH="/home/miy1z1ki/ffmpeg_build/lib/pkgconfig" ./configure --prefix="/home/miy1z1ki/ffmpeg_build" --bindir="/home/miy1z1ki/bin" --enable-static --enable-pic && \
make && \
make install

apt-get install mercurial libnuma-dev && \
cd /home/miy1z1ki/ffmpeg_sources && \
if cd x265 2> /dev/null; then hg pull && hg update && cd ..; else hg clone https://bitbucket.org/multicoreware/x265; fi && \
cd x265/build/linux && \
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="/home/miy1z1ki/ffmpeg_build" -DENABLE_SHARED=off ../../source && \
make && \
make install 

git -C libvpx pull 2> /dev/null || git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git && \
cd libvpx && \
./configure --prefix="home/miy1z1ki/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
make && \
make install
============
git -C fdk-aac pull 2> /dev/null || git clone --depth 1 https://github.com/mstorsjo/fdk-aac && \
cd fdk-aac && \
autoreconf -fiv && \
./configure --prefix="/home/miy1z1ki/ffmpeg_build" --disable-shared && \
make && \
make install

git -C opus pull 2> /dev/null || git clone --depth 1 https://github.com/xiph/opus.git && \
cd opus && \
./autogen.sh && \
./configure --prefix="/home/miy1z1ki/ffmpeg_build" --disable-shared && \
make && \
make install

PKG_CONFIG_PATH="/home/miy1z1ki/ffmpeg_build/lib/pkgconfig"
./configure \
  --prefix="/home/miy1z1ki/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I/home/miy1z1ki/ffmpeg_build/include" \
  --extra-ldflags="-L/home/miy1z1ki/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --bindir="/home/miy1z1ki/bin" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-nonfree && \
make && \
make install && \
hash -r

source ~/.profile

神tmd编译成功了，，，

https://github.com/floyd-fuh/afl-crash-analyzer/blob/master/testcases/ffmpeg/install.sh 

CC="/usr/local/bin/afl-clang" CXX="/usr/local/bin/afl-clang++" ./configure --prefix="/home/miy1z1ki/ffmpeg_build" --pkg-config-flags="--static" --extra-cflags="-I/home/miy1z1ki/ffmpeg_build/include -c -fsanitize=address -O0 -g -v" --extra-cxxflags="-I/home/miy1z1ki/ffmpeg_build/include -c -fsanitize=address -O0 -g -v" --extra-ldflags="-L/home/miy1z1ki/ffmpeg_build/lib -fsanitize=address" --extra-libs="-lpthread -lm" --bindir="/home/miy1z1ki/bin" --enable-gpl --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libvorbis --enable-libvpx --enable-nonfree   

1 去掉支持的多余的音乐
2 增加ASAN

修改 afl文件后缀，重新编译afl
afl-analyze          afl-as.h       afl-cmin     afl-gcc     afl-plot      afl-tmin.c     config.h     experimental  llvm_mode      types.h
root@9b798cc2ff72:/usr/local/bin# grep "cur_input" ./*.c 
./afl-fuzz.c:  fn = alloc_printf("%s/.cur_input", out_dir);
./afl-fuzz.c:  u8* fn = alloc_printf("%s/.cur_input", out_dir);
./afl-fuzz.c:        out_file = alloc_printf("%s/.cur_input", out_dir);

