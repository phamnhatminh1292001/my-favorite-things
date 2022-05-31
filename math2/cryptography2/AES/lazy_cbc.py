from Crypto.Cipher import AES
import requests
import os
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes
key = b'Sixteen byte key'


def encrypt(plaintext):
    url = "http://aes.cryptohack.org/lazy_cbc/encrypt/"
    r = requests.get(url+plaintext+'/')
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

def get_flag(key):
    url = "http://aes.cryptohack.org/lazy_cbc/get_flag/"
    r = requests.get(url+key+'/')
    return r.json()['plaintext']

def xor(s1,s2):
    str=""
    i=0
    while (i<len(s1)):
        str+=hex(int(s1[i],16)^int(s2[i],16))[2:]
        i+=1
    return str

def receive(ciphertext):
    url = "http://aes.cryptohack.org/lazy_cbc/receive/"
    r = requests.get(url+ciphertext+'/')
    t=r.json()
    return [t['error'][19:51],t['error'][51:83]]

# we can input any string c1c2
# dec: m1=f(c1)^key  m2=f(c2)^c1 
#  we need to find the key, but we don't know f(c1) and f(c2)
# then let c1=c2 and done
#key=m1^m2^c1


m=receive(bytes.hex(b'0'*32))
xor1=xor(m[0],m[1])
key=xor(bytes.hex(b'0'*16),xor1)
decrypted_hex=get_flag(key)
print(bytes.fromhex(decrypted_hex))