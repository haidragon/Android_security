FFmpeg 漏洞
1. CVE-2017-11399
	'libavcodec/apedec.c' 
FFmpeg <= 3.3.2版本，libavcodec/apedec.c/ape_decode_frame函数存在安全漏洞，可使远程攻击者通过构造的APE文件，利用此漏洞造成拒绝服务。

2. CVE-2017-14767
FFmpeg 3.3.4之前版本，libavformat/rtpdec_h264.c/sdp_parse_fmtp_config_h264函数未正确处理空sprop-parameter-sets值，可使远程攻击者通过构造的sdp文件，造成拒绝服务（堆缓冲区溢出）。

3. CVE-2017-11399
2017-07-17
影响3.3.2版本之前的 libavcodec/apedec.c 中的 ape_decode_frame 函数，整数溢出允许远程攻击者通过精心设计的APE文件导致拒绝服务（阵外访问和应用程序崩溃）或可能具有未指定的其他影响。

4. CVE-2017-11719、CVE-2017-11665、CVE-2017-11399、CVE-2017-9608 
libavcodec/dnxhddec.c、libavformat/rtmppkt.c、 libavcodec/apedec.c 、via a crafted mov file
DoS攻击

x.  FFmpeg任意文件读取漏洞分析
利用了ffmpeg可以处理 HLS 播放列表的功能，在 AVI 文件中的 GAB2字幕块中嵌入了一个 HLS 文件，然后提供给ffmpeg进行转码，在解析的过程中把它当做一个 XBIN 的视频流来处理，再通过 XBIN 的编解码器把本地的文件包含进来，最后放在转码后的视频文件当中。
ref：
https://www.freebuf.com/column/142775.html
ppt：
https://docs.google.com/presentation/d/1yqWy_aE3dQNXAhW8kxMxRqtP7qMHaIfMzUDpEqFneos/edit#slide=id.g1e10cfbccc_0_26

5. Monkey's Audio
Version 4.64 (April 15, 2019)
Fixed: Tagging could crash.

Version 4.57 (March 14, 2019)
Fixed: Corrected a couple more corrupt file crash issues (thanks Piotr Pawlowski).

Version 4.47 (February 24, 2019)
Fixed: Corrected another crash bug in handling corrupt files.
Fixed: Better handling of memory allocation errors.

Version 4.45 (February 23, 2019)
Fixed: Improved handling of corrupt APE files to avoid crashes (files with invalid blocks per frame, invalid block align, etc.).

Version 4.39 (November 11, 2018)
Fixed: A corrupt APE file with a negative number for the WAV header length could crash instead of being handled gracefully.
Fixed: Corrected a couple compiler warnings.

