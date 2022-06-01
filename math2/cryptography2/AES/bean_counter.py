from Crypto.Cipher import AES
import requests
import os
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes


def encrypt():
    url = "http://aes.cryptohack.org//bean_counter/encrypt/"
    r = requests.get(url)
    return r.json()['encrypted']


class StepUpCounter(object):
    def __init__(self, value=os.urandom(16), step_up=False):
        self.value = value.hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value


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

#the keystream is repeated after every 16 bytes because step_up=False
#thus c[i]=m[i]^f(iv) for all i, we just need to know the f(iv)
#we know the first 16 bytes of the PNG, thus we should know the f(iv)
png_first_bytes=b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52'
h=bytes.hex(png_first_bytes)
enc=encrypt()
enclist=split(enc)[0]
func_iv=xor(h,enclist)
i=0
s=""
while (i<len(enc)):
    s+=func_iv
    i+=32
plaintext=xor(enc,s)
plaintext=bytes.fromhex(plaintext)
with open('bean.png', 'wb') as f:
    f.write(bytes(plaintext))

#reference: https://stackoverflow.com/questions/54845745/not-able-to-read-ihdr-chunk-of-a-png-file