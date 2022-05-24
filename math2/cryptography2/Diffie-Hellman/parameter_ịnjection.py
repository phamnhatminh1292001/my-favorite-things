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
PORT = 13371


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

#solution: we just need to modify their common key into some value
# we could control
# when we send (p2,g2,A2) to Bob, key1=pow(A2,b,p2)
# when we send B2 to Alice, key2=pow(B2,a,p)
# we need key1=key2, the easiest way to do is to set A2=B2=1, p2=p
q=readline().decode()
s=take_dict(q)
p=s['p']
g=s['g']
A=s['A']
id='0x1'
request={'p':p,'g':g,'A':id}
json_send(request)
q=readline().decode()
s=take_dict(q)
B=s['B']
request={'B':id}
json_send(request)
q=readline().decode()
s=take_dict(q)
iv1=s['iv']
encrypted_flag1=s['encrypted_flag']
key=1
m=decrypt_flag(key,iv1,encrypted_flag1)
print(m)
