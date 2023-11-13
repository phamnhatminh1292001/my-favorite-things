#!/usr/bin/env python3
from unicodedata import decimal
import pwn
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
import hashlib
from pkcs1 import emsa_pkcs1_v15
HOST = "socket.cryptohack.org"
PORT = 13376
import gmpy2

ADMIN_TOKEN = b"admin=True"
pr = telnetlib.Telnet(HOST, PORT)

def readline():
    return pr.read_until(b"\n")

def json_send(hsh):
    request = json.dumps(hsh).encode()
    pr.write(request)


def json_recv():
    line = readline()
    return json.loads(line.decode())

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
    str=json.loads(str)
    return str

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))



# we need to send a message m such that c1=m^d (mod N) and c1^e (mod N)=ADMIN_TOKEN
# but m != ADMIN_TOKEN, then just send m=ADMIN_TOKEN+N
q=readline()
print(q)
request={"option":"get_pubkey"}
json_send(request)
q=readline().decode()
s=take_dict(q)
N=int(s['N'],16)
e=int(s['e'],16)
ADMIN_TOKEN = b"admin=True"
m=bytes_to_long(ADMIN_TOKEN)+N
m=hex(m)[2:]
request={"option":"sign",'msg':m}
json_send(request)
q=readline().decode()
s=take_dict(q)
sign=int(s['signature'],16)
sign=hex(sign)[2:]
m2=hex(bytes_to_long(ADMIN_TOKEN))[2:]
request={"option":"verify",'msg':m2,'signature':sign}
json_send(request)
q=readline().decode()
print(q)






