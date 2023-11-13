import pwn
import json
import hashlib
import re
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, inverse, isPrime

a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
p = 2**256 - 2**224 + 2**192 + 2**96 - 1


def json_recv():
    line = r.recvline()
    line=line.decode()
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def xor(c, m):
    return bytes([x ^ y for x, y in zip(m.ljust(64, b"\0"), c)])

quotes = [
    "Konpeko, konpeko, konpeko! Hololive san-kisei no Usada Pekora-peko! domo, domo!",
    "Bun bun cha! Bun bun cha!",
    "kitira!",
    "usopeko deshou",
    "HA↑HA↑HA↓HA↓HA↓",
    "HA↑HA↑HA↑HA↑",
    "it's me pekora!",
    "ok peko",
]

r=pwn.connect('archive.cryptohack.org',45328)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=line.split(" ")
xpub=int(line[4][1:-1])
ypub=int(line[5][:-2])
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
json_send(2)
line=json_recv()
print(line)
xC1=int(line[2:66],16)
yC1=int(line[66:],16)
line=json_recv()
print(line)
C2=bytes.fromhex(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
json_send(1)
line=json_recv()
print(line)
json_send(xC1)
json_send(yC1)
line=json_recv()
print(line)
enc=line[6:]
enc=bytes.fromhex(enc)
lst=[]
for i in quotes:
    lst.append(xor(enc,i.encode()))
u=v=0
for i in lst:
    u=bytes_to_long(i[:len(i)//2])
    v=bytes_to_long(i[len(i)//2:])
    if (v**2-u**3-a*u-b)%p==0:
        break
shared=long_to_bytes(u)+long_to_bytes(v)
flag=xor(shared,C2)
print(flag)