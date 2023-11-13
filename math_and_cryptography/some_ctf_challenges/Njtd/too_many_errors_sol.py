import pwn
import json
from Crypto.Random.random import getrandbits
import random
import string
alphabet = '}'+'{'+'_'+string.ascii_lowercase+string.ascii_uppercase+string.digits
SEED = getrandbits(32)
FLAG = b'crypto{????????????????????}'
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
r=pwn.connect('socket.cryptohack.org',13390)
line=json_recv()
print(line)
request={"option":"get_sample"}
json_send(request)
line=json_recv()
s=take_dict(line)
a1=s["a"]
b1=s["b"]
dict={}

while True:

    request={"option":"get_sample"}
    json_send(request)
    line=json_recv()
    s=take_dict(line)
    a2=s["a"]
    b2=s["b"]
    if b2 != b1:
        for i in range(0,len(a1)):
            if a2[i] != a1[i]:
                t=chr((b2-b1)*pow(a2[i]-a1[i],-1,127)%127)
                if t in alphabet:
                    dict[i]=t
                break
    if len(dict)==len(FLAG):
        break
    request={"option":"reset"}
    json_send(request)
    line=json_recv()
s=""
for i in range (0,len(dict)):
    s+=dict[i]
print(s)