#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import base64
import hashlib
import codecs
import struct
import pdb

def AES_encode(source,iv,key,PADDING):
	pad_it = lambda s: s+(16 - len(s)%16)*PADDING  

	generator = AES.new(key, AES.MODE_CBC, iv)

	crypt = generator.encrypt(pad_it(source))  

	cryptedStr = base64.b64encode(crypt)

	return cryptedStr

def AES_decode(crypt,iv,key,PADDING):
	generator = AES.new(key, AES.MODE_CBC, iv)

	recovery = generator.decrypt(crypt)
	#print(recovery.rstrip(PADDING))
	return recovery

#def key_md5(key):
#	k_md5 = hashlib.md5(key).hexdigest()
#	retun k_md5
# apk 头部 504b 0304
def filetype(binfile):  
    #binfile = open(filename, 'rb') # 必需二制字读取  
    flag = 0  
    ftype = 'PK\x03\x04'   
    '\x50\x4b\x03\x04'
    numOfBytes = 4 # 需要读多少字节 
    if binfile[0:4] == 'PK\x03\x04':
    	flag = 1
    return flag
    #f_hcode = bytes2hex(hbytes)  
 
    #return ftype

def main():
	PADDING = '\0'

	#initVector = [19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55]
	iv = '\x13\x37\x13\x37\x13\x37\x13\x37\x13\x37\x13\x37\x13\x37\x13\x37'
	#source = 'test string'

	#key
	str_key = ''
	t0 = t1 = t2 = t3 = 0
	for t0 in range(127,0,-1):
		for t1 in range(127,0,-1):
			for t2 in range(127,0,-1):
				for t3 in range(127,0,-1):
					str_key = chr(t0) + chr(t1) + chr(t2) + chr(t3)
					str_key_md5 = hashlib.md5(str_key).hexdigest()
					
					crypt = open('/Users/miy1z1ki/Desktop/Android_security/apk/vitor/assets/ckxalskuaewlkszdva','rb')
					all_crypt = crypt.read( )
					crypt.close()

					cryptedStr = AES_decode(all_crypt,iv,str_key_md5,PADDING)
					cflag = filetype(cryptedStr)
					if cflag :
						print("## pass first fire wall : ",str_key)
						break
					if t3 % 30  == 0 :
						print('## loading... ', str_key )
					#cryptedStr = AES_encode(source,iv,str_key_md5,PADDING)
					#AES_decode(source,iv,str_key_md5,PADDING,crypt)



if __name__ == '__main__':
	main()





