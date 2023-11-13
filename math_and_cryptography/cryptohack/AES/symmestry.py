from Crypto.Cipher import AES
import requests
import os
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes


def encrypt(plaintext,iv):
    url = "http://aes.cryptohack.org/symmetry/encrypt/"
    r = requests.get(url+plaintext+'/'+iv+'/')
    return r.json()['ciphertext']

def encrypt_flag():
    url = "http://aes.cryptohack.org/symmetry/encrypt_flag/"
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
    if len(s)%32 !=0:
        b=b-32
        list.append(s[b:])
    return list

def xor(s1,s2):
    str=""
    i=0
    while (i<len(s1)):
        str+=hex(int(s1[i],16)^int(s2[i],16))[2:]
        i+=1
    return str

# f1=f(iv)  c1=f1^m1
# f2=f(f1)  c2=f2^m2
# f3=f(f2)  c3=f3^m3
enc=encrypt_flag()
enclist=split(enc)
enc2=encrypt(bytes.hex(b'\x00'*33),enclist[0])
enclist2=split(enc2)
m1=xor(enclist2[0],enclist[1])
m2=xor(enclist2[1],enclist[2])
m3=xor(enclist2[2],enclist[3])
m4=bytes.fromhex(m1+m2+m3)
print(m4)

