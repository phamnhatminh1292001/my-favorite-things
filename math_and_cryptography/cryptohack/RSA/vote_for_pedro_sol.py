
from Crypto.Util.number import bytes_to_long, long_to_bytes
import math
from sympy import *
import telnetlib
import json
HOST = "socket.cryptohack.org"
PORT = 13375

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
e = 3

q=readline().decode()

m=b'VOTE FOR PEDRO'
m=bytes_to_long(m)
decrypted=long_to_bytes(m)
print(decrypted)
m3=pow(2,8*15)
def Hensel(m,p,e):
    x0=0
    for i in range(0,e):
        for c in range(0,p):
            if ((x0+c*p**i)**3-m)%(p**(i+1))==0:
                x0=x0+c*p**i
    return x0
c=Hensel(m,2,8*15)
c=hex(c)[2:]

request={'option':'vote','vote':c}
json_send(request)
q=readline().decode()
print(q)