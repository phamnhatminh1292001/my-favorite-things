from Crypto.Cipher import AES
import requests
import os
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes

def encrypt():
    url = "http://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/"
    r = requests.get(url)
    return r.json()['ciphertext']

def split(s):
    a=0
    b=32
    list=[]
    while (b<=len(s)):
        list.append(s[a:b])
        a+=32
        b+=32
    return list

def decrypt(ciphertext):
    url = "http://aes.cryptohack.org/ecbcbcwtf/decrypt/"
    r = requests.get(url + ciphertext + '/')
    return r.json()['plaintext']



enc=encrypt()
enc=split(enc)
ciphertext=enc[1]+enc[2]
dec=decrypt(ciphertext)
dec=split(dec)
enc1=[int(i,16) for i in enc]
dec1=[int(i,16) for i in dec]
msg=b""
for i in range(0,len(dec1)):
    msg+=long_to_bytes(enc1[i]^dec1[i])
print(msg)