import pwn
import json
import time
import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from datetime import datetime
from random import randrange
g = generator_192
n = g.order()

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
    line = z.recvline()
    line=line.decode()
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    z.sendline(request)

def sha1(data):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(data)
        return sha1_hash.digest()



r=0
s=0
z=pwn.connect('socket.cryptohack.org',13381)
line=json_recv()
msg=""
msg1=0
found=False
while found==False:    
    request={"option":"sign_time"}
    json_send(request)
    line=json_recv()
    print(line)
    dict=take_dict(line)
    r=int(dict["r"],16)
    s=int(dict["s"],16)
    msg=dict["msg"] 
    msg1=int(dict["msg"].split(":")[1])
    if (msg1<5):
        found=True
    u=(1-msg1)%60
    if found==False:
        time.sleep(u)


for i in range(1,msg1):
    secret=(s*i-bytes_to_long(sha1(msg.encode())))*pow(r,-1,n)%n
    print(secret)
    pubkey = Public_key(g, g * secret)
    privkey = Private_key(pubkey, secret)
    newmsg = f"unlock"
    hsh = sha1(newmsg.encode())
    sig = privkey.sign(bytes_to_long(hsh), randrange(1, 2))
    request={"option":"verify","msg":"unlock","r":hex(sig.r),"s":hex(sig.s)}
    json_send(request)
    line=json_recv()
    print(line)