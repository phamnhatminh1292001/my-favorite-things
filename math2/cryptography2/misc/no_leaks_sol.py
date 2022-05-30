#!/usr/bin/env python3
from asyncio.constants import ACCEPT_RETRY_DELAY
import os
from Crypto.Util.number import bytes_to_long, long_to_bytes
from pkcs1 import emsa_pkcs1_v15
import string
import json
import pwn
import base64
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

#it was stupid to ensure that no bytes from the flags are leaked.


alphabet = '_'+'@'+string.digits+string.ascii_lowercase+string.ascii_uppercase
ordlist=[ord(x) for x in alphabet]
l=len(ordlist)
dict={}
for i in range (7,19):
    dict[i]=[]




while True:
                r = pwn.connect('socket.cryptohack.org', 13370)
                q=json_recv()
                request={'msg':'request'}
                json_send(request)
                q=json_recv()
                s=take_dict(q)
                if not 'error' in s:
                    receive=[x for x in base64.b64decode(s['ciphertext'])]
                    for i in range(7,19):
                        if (receive[i] in ordlist) and (receive[i] not in dict[i]):
                            dict[i].append(receive[i])
                    found=True
                    for i in range(7,19):
                        if len(dict[i]) !=l-1:
                            found=False
                            break
                    if found==True:
                        break
                r.close()

ordflag=[]
for i in dict:
    for j in ordlist:
        if j not in dict[i]:
            ordflag.append(j)
decrypted=""
for i in ordflag:
    decrypted+=chr(i)
decrypted='crypto{'+decrypted+'}'
print(decrypted)



