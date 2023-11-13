#!/usr/bin/env python3
import pwn
import json
import hashlib
import re
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse, isPrime
from pkcs1 import emsa_pkcs1_v15
# from params import N, E, D

FLAG = b"crypto{????????????????????????????????????}"

BIT_LENGTH = 768

MSG = b'We are hyperreality and Jack and we own CryptoHack.org'
DIGEST = emsa_pkcs1_v15.encode(MSG, BIT_LENGTH // 8)
BTC_PAT = re.compile("^Please send all my money to ([1-9A-HJ-NP-Za-km-z]+)$")


def xor(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def btc_check(msg):
    alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    addr = BTC_PAT.match(msg)
    if not addr:
        return False
    addr = addr.group(1)
    raw = b"\0" * (len(addr) - len(addr.lstrip(alpha[0])))
    res = 0
    for c in addr:
        res *= 58
        res += alpha.index(c)
    raw += long_to_bytes(res)

    if len(raw) != 25:
        return False
    if raw[0] not in [0, 5]:
        return False
    return raw[-4:] == hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4]


PATTERNS = [
    re.compile(r"^This is a test(.*)for a fake signature.$").match,
    re.compile(r"^My name is ([a-zA-Z\s]+) and I own CryptoHack.org$").match,
    btc_check
]





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
    return json.loads(str)

def json_recv():
    line = r.recvline()
    line=line.decode()
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def finde(m,c):
    e=0
    for i in range(0,40):
        if (pow(m,i,41)==c%41):
            e=i
            break
    for i in range(1,190):
        for j in range (0,41):
            if (pow(m,e+j*40*41**(i-1),41**(i+1))==c%(41**(i+1))):
                e+=j*40*41**(i-1)
                break
    return e

r=pwn.connect('socket.cryptohack.org',13394)
line=json_recv()
request={'option':'get_signature'}
json_send(request)
line=json_recv()
s=take_dict(line)
signature=int(s['signature'],16)
N=41**190
print(N.bit_length())
msg1="This is a test.for a fake signature."
msg2="My name is M and I own CryptoHack.org"
msg3="Please send all my money to 1KFaWFgzm6nppjvMDNLrzfoY7UGo7xekvx"
t=btc_check(msg3)
request={'option':'set_pubkey','pubkey':hex(N)}
json_send(request)
line=json_recv()
print(line)
s=take_dict(line)
suffix=s["suffix"]
msg1+=suffix
msg2+=suffix
msg3+=suffix

digest1 = emsa_pkcs1_v15.encode(msg1.encode(), BIT_LENGTH // 8)
digest1=bytes_to_long(digest1)
e=finde(signature,digest1)
request={'option':'claim','e':hex(e),'index':0,'msg':msg1}
json_send(request)
line=json_recv()
s=take_dict(line)
print(line)
SECR0=bytes.fromhex(s["secret"])


digest2 = emsa_pkcs1_v15.encode(msg2.encode(), BIT_LENGTH // 8)
digest2=bytes_to_long(digest2)
e=finde(signature,digest2)
request={'option':'claim','e':hex(e),'index':1,'msg':msg2}
json_send(request)
line=json_recv()
s=take_dict(line)
print(line)
SECR1=bytes.fromhex(s["secret"])

digest3 = emsa_pkcs1_v15.encode(msg3.encode(), BIT_LENGTH // 8)
digest3=bytes_to_long(digest3)
e=finde(signature,digest3)
request={'option':'claim','e':hex(e),'index':2,'msg':msg3}
json_send(request)
line=json_recv()
s=take_dict(line)
print(line)
SECR2=bytes.fromhex(s["secret"])

m=xor(xor(SECR2,SECR1),SECR0)
print(m)