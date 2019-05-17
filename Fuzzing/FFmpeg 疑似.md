# FFmpeg 疑似
1. https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/dxv.c#L889
这个地方可能存在out-of-array问题或者eof问题
out-of-array问题

EOF（文件结束符）问题
1、文件指针
当打开文件时，文件指针位置为0，
2、关于EOF（换行键）
很多朋友认为文件尾有EOF，这是错误的。EOF是流的状态标志。在 C++中，是在读取文件失败时才产生EOF。所以第一个程序中，在输出第一个b时，产生了EOF，再输出第二个b时读取到EOF，循环结束。

line 889 if (bytestream2_get_bytes_left(gbc) < 1)

check bytestream2_get_le32 读几个字节是1个还是4个

