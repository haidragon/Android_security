# FFmpeg多媒体文件格式探测
此处审计libavformat的avformat_open_input

FFmpeg中实现探测的函数是av_probe_input_buffer2和av_probe_input_format3。其核心代码如下：
'''
	//遍历所有的Demuxer
	while ((fmt1 = av_demuxer_iterate(&i))) {
	        if (!is_opened == !(fmt1->flags & AVFMT_NOFILE) && strcmp(fmt1->name, "image2"))
	            continue;
	        score = 0;
	        if (fmt1->read_probe) {
	            score = fmt1->read_probe(&lpd);
	            if (score)
	                av_log(NULL, AV_LOG_TRACE, "Probing %s score:%d size:%d\n", fmt1->name, score, lpd.buf_size);
	            if (fmt1->extensions && av_match_ext(lpd.filename, fmt1->extensions)) {
	                switch (nodat) {
	                case NO_ID3:
	                    score = FFMAX(score, 1);
	                    break;
	                case ID3_GREATER_PROBE:
	                case ID3_ALMOST_GREATER_PROBE:
	                    score = FFMAX(score, AVPROBE_SCORE_EXTENSION / 2 - 1);
	                    break;
	                case ID3_GREATER_MAX_PROBE:
	                    score = FFMAX(score, AVPROBE_SCORE_EXTENSION);
	                    break;
	                }
	            }
	        } else if (fmt1->extensions) {
	            if (av_match_ext(lpd.filename, fmt1->extensions))
	                score = AVPROBE_SCORE_EXTENSION;
	        }
	        if (av_match_name(lpd.mime_type, fmt1->mime_type)) {
	            if (AVPROBE_SCORE_MIME > score) {
	                av_log(NULL, AV_LOG_DEBUG, "Probing %s score:%d increased to %d due to MIME type\n", fmt1->name, score, AVPROBE_SCORE_MIME);
	                score = AVPROBE_SCORE_MIME;
	            }
	        }
	        if (score > score_max) {
	            score_max = score;
	            fmt       = (AVInputFormat*)fmt1;
	        } else if (score == score_max)
	            fmt = NULL;
	    }
'''

优先使用demuxer的read_probe函数，然后参考文件名的后缀名来关联某个AVInputFormat。
