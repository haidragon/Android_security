# 动态调试 ffmpeg
重点在于看 ffmpeg 编解码 ape的流程
./gdb ffmpeg_g
set args -i ../ffmpeg/fuzz_in/Michel_Telo.ape test.mp3
b main
run
b xxx/ape_xxx
=================

首先到达 ape_probe 
（会不会存在，畸形ape，实际为ape，但是设置被探测为非ape，使用其他格式的demuxer进行解码，crash）

确认 有没有对头部进行check
。
=================

'''
gdb-peda$ bt
#0  ape_read_header (s=0x1f599c0) at libavformat/ape.c:171
#1  0x000000000079aea6 in avformat_open_input (ps=ps@entry=0x7fffffffdee8, filename=filename@entry=0x7fffffffe85b "../ffmpeg/fuzz_in/Michel_Telo.ape", 
    fmt=fmt@entry=0x0, options=0x1f54f48) at libavformat/utils.c:631
#2  0x000000000048a724 in open_input_file (o=o@entry=0x7fffffffe080, filename=<optimized out>) at fftools/ffmpeg_opt.c:1104
#3  0x000000000048c3dc in open_files (l=0x1f54e58, l=0x1f54e58, open_file=0x488d40 <open_input_file>, inout=0x11441b1 "input")
    at fftools/ffmpeg_opt.c:3273
#4  ffmpeg_parse_options (argc=argc@entry=0x4, argv=argv@entry=0x7fffffffe618) at fftools/ffmpeg_opt.c:3313
#5  0x000000000048466d in main (argc=argc@entry=0x4, argv=argv@entry=0x7fffffffe618) at fftools/ffmpeg.c:4872
#6  0x00007ffff40cf830 in __libc_start_main (main=0x4845e0 <main>, argc=0x4, argv=0x7fffffffe618, init=<optimized out>, fini=<optimized out>, 
    rtld_fini=<optimized out>, stack_end=0x7fffffffe608) at ../csu/libc-start.c:291
#7  0x0000000000484909 in _start ()
'''

经过了 
ffmpeg.c:0x000000000048466d
调用 ffmpeg_opt.c:ffmpeg_parse_options
调用 open_files ->
open_input_file ->
utils.c:avformat_open_input -> 
ape.c -> ape_read_header
