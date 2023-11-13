import pwn
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
import hashlib
from sympy import *
import math
from pkcs1 import emsa_pkcs1_v15

r = pwn.connect('socket.cryptohack.org', 13391)
def take_dict(s):
    m=0
    n=0
    for i in range(0,len(s)):
        if s[i]=="{":
            m=i
        if s[i]=="}":
            n=i
    str=""        
    for i in range(m,n+1):
        str=str+s[i]
    if str[0]!="{":
        return s
    return json.loads(str)

def json_recv():
    line = r.recvline()
    line=line.decode()
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

#we are given a signature sign
#we can input 3 values e,n and msg such that 
#m=bytes_to_long(emsa_pkcs1_v15.encode(mymsg.encode(), 256))
#and m=sign^e (mod n)
#well, since we can control e and n we just need to find n such
#that m=e(mod n) then n=m-e, done.


q=json_recv()
request={'option':'get_signature'}
json_send(request)
q=json_recv()
s=take_dict(q)
sign=int(s['signature'],16)
N1=int(s['N'],16)
mymsg="I am Malloryown CryptoHack.org"
digest = bytes_to_long(emsa_pkcs1_v15.encode(mymsg.encode(), 256))
N=sign-digest
request={'option':'verify','N':hex(N),'e':hex(1),'msg':mymsg}
json_send(request)
q=json_recv()
print(q)


