#!/usr/bin/env python3
from unicodedata import decimal
import pwn
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
import hashlib
HOST = "socket.cryptohack.org"
PORT = 13374
import gmpy2

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

#if your option is "sign", and your input is s, you will receive s^d (mod N)
#you have m^e (mod N), then just let s=m^e and you get m. Done
q=readline()
print(q)
request={"option":"get_pubkey"}
json_send(request)
q=readline().decode()
s=take_dict(q)
N=int(s['N'],16)
e=int(s['e'],16)
request={"option":"get_secret"}
json_send(request)
q=readline().decode()
s=take_dict(q)
c=int(s['secret'],16)

request={"option":"sign","msg":hex(c)}
json_send(request)
q=readline().decode()
s=take_dict(q)
t=int(s['signature'],16)
t=long_to_bytes(t)
print(t)



