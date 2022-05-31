from Crypto.Cipher import AES
import requests
import os
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes
key = b'Sixteen byte key'


def check_admin(cookie,iv):
    url = "http://aes.cryptohack.org/flipping_cookie/check_admin/"
    r = requests.get(url+cookie+'/'+iv+'/')
    return r.json()['flag']

def split(s):
    a=0
    b=32
    list=[]
    while (b<=len(s)):
        list.append(s[a:b])
        a+=32
        b+=32
    return list

def get_cookie():
    url = "http://aes.cryptohack.org/flipping_cookie/get_cookie/"
    r = requests.get(url)
    return r.json()['cookie']

def xor(s1,s2):
    str=""
    i=0
    while (i<len(s1)):
        str+=hex(int(s1[i],16)^int(s2[i],16))[2:]
        i+=1
    return str

enc=get_cookie()
enc=split(enc)
ciphertext=enc[1]+enc[2]
false='0'*12+hex(ord('F'))[2:]+hex(ord('a'))[2:]+hex(ord('l'))[2:]+hex(ord('s'))[2:]+hex(ord('e'))[2:]+'0'*10
true='0'*12+hex(ord('T'))[2:]+hex(ord('r'))[2:]+hex(ord('u'))[2:]+hex(ord('e'))[2:]+hex(ord(';'))[2:]+'0'*10
modify=xor(false,true)
iv=xor(enc[0],modify)
decrypted=check_admin(ciphertext,iv)
print(decrypted)