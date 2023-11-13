#!/usr/bin/env python3
import pwn
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
HOST = "socket.cryptohack.org"
PORT = 13403


pr = telnetlib.Telnet(HOST, PORT)

def readline():
    return pr.read_until(b"\n")

def json_send(hsh):
    request = json.dumps(hsh).encode()
    pr.write(request)


# we need to find two integers a and n such that n | a^q-1 and n does not divide a-1
# we cannot compute a^q-1, therefore we need to think of two integers without computing anything
# we can choose a=q+1 and n=q^2


q = readline().split(b'"')
q=q[1]
q=q.decode()

q=int(q,0)

m2=q+1
m2=hex(m2)
m3=q*q
m3=hex(m3)
request = {
    "g": m2,
    "n": m3
}
json_send(request)

x = readline().split(b'"')
x=x[1]
x=x.decode()

x=int(x,0)
x=(x-1)//q
x=hex(x)

request = {
    "x": x,
}
json_send(request)

a=readline()
print(a)
