import json
from hashlib import sha512
from Crypto.Util.number import bytes_to_long, long_to_bytes, isPrime
from Crypto.Hash import MD5
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

data=b'\x00'*8
data2=b'\x00'*3+b'\x80'+b'\x00'*3+long_to_bytes(240^155)
r=pwn.connect('socket.cryptohack.org',13395)
json_recv()
request={'a':data.hex(),'b':data2.hex()}
json_send(request)
line=json_recv()
print(line)