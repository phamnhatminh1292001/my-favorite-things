from Crypto.Util.number import getPrime, inverse, bytes_to_long
import string
import requests
import zlib

def encrypt(plaintext):
    url = "http://aes.cryptohack.org/ctrime/encrypt/"
    r = requests.get(url+plaintext+'/')
    return r.json()['ciphertext']

#according to the hints I received on Discord, compressing repeated characters
#may cause the length of the string unchanged, but it is not always true
#but it has a high chance to happen, thus if we insert repeated characters, and
#the length of the encrypted string does not change, then the character is in 
#the flag.


alphabet = '}'+'_'+string.ascii_uppercase+string.digits+string.ascii_lowercase
str=b'crypto{CRIME'
enc=encrypt(str.hex())
while True:
    for i in alphabet:
        enc2=encrypt(str.hex()+i.encode().hex())
        if len(enc)==len(enc2):
            str+=i.encode()
            break
    if str[-1]==b'}':
        break
