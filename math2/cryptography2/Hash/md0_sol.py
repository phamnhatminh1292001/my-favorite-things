from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import json
import pwn


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

def hash(data):
    data = pad(data, 16)
    out = b"\x00" * 16
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
        print(out)
    return out

def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


r=pwn.connect('socket.cryptohack.org',13388)
json_recv()
request={'option':'sign','message':'0'*32}
json_send(request)
line=json_recv()
s=take_dict(line)
enc=s['signature']
enc=bytes.fromhex(enc)
next=bxor(AES.new(b'admin=True000000', AES.MODE_ECB).encrypt(enc), enc)
next=bxor(AES.new(b'\x10'*16, AES.MODE_ECB).encrypt(next), next)
next=next.hex()
m2=b'admin=True000000'.hex()
request={'option':'get_flag','message':'0'*32+'10'*16+m2,'signature':next}
json_send(request)
line=json_recv()
print(line)