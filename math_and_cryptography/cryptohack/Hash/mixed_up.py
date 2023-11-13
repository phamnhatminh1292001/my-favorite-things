from Crypto.Util.number import long_to_bytes
import os
from hashlib import sha256
import json
import pwn
FLAG = b"crypto{???????????????????????????????}"
def _xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

def _and(a, b):
    return bytes([_a & _b for _a, _b in zip(a, b)])

def shuffle(mixed_and, mixed_xor):
    return bytes([mixed_xor[i%len(mixed_xor)] for i in mixed_and])

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


lst=[long_to_bytes(i)*len(FLAG) for i in range (0,255)]
lst=[sha256(i).hexdigest() for i in lst]
bittry=[]
for i in range (0,8*len(FLAG)):
    bittry.append("0"*i+"1"+"0"*(8*len(FLAG)-i-1))
bittry=[f'{int(i, 2):X}' for i in bittry]
print(len(bittry[0]))
for i in range(0,len(bittry)):
    bittry[i]="0"*(len(bittry[0])-len(bittry[i]))+bittry[i]
bitlist=""
r=pwn.connect('socket.cryptohack.org',13402)
json_recv()
for i in range(0,8*len(FLAG)):
    request={"option":"mix","data":bittry[i]}
    json_send(request)
    line=json_recv()
    s=take_dict(line)
    s=s["mixed"]
    if s in lst:
        bitlist+="0"
    else:
        bitlist+="1"
decrypt=int(bitlist,2)
decrypt=long_to_bytes(decrypt)
print(decrypt)

