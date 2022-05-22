#!/usr/bin/env python3
from unicodedata import decimal
import pwn
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
import hashlib
HOST = "socket.cryptohack.org"
PORT = 13380


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

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

#one question remain: why can't I do with key=0? I send B=0 to Alice
# and let key=0 and for some reason it does not work.

id=hex(0)
q=readline().decode()
print(q)
s=take_dict(q)
p=s['p']
g=s['g']
A=s['A']
p1=int(p,16)
g1=int(g,16)
A1=int(A,16)
g1=pow(g1,-1,p1)
a=(A1*g1)%p1

request={'p':p,'g':g,'A':A}
json_send(request)
q=readline().decode()
print(q)
s=take_dict(q)
B=s['B']
B1=int(B,16)
b=(B1*g1)%p1
print((B1*a-A1*b)%p1)
request={'B':B}
json_send(request)
q=readline().decode()
print(q)
s=take_dict(q)
iv1=s['iv']
encrypted_flag1=s['encrypted']
key=A1*b%p1
m=decrypt_flag(key,iv1,encrypted_flag1)
print(m)