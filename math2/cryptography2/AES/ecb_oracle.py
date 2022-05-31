from Crypto.Cipher import AES
import requests
import time
import string
from Crypto.Util.Padding import pad, unpad


def encrypt(plaintext):
    url = "http://aes.cryptohack.org/ecb_oracle/encrypt/"
    r = requests.get(url + plaintext + '/')
    return r.json()['ciphertext']
alphabet = '}'+'_'+string.ascii_lowercase+string.ascii_uppercase+string.digits



#how ECB works: divide into 16 bytes blocks
#we can insert some string at the beginning of the flag
#the key is what should we insert?
#Well, we can insert some 1s at the beginning of the flag until the padded
#text has size divisible by 16, get the result and then brute force, done.
#but we don't know the len of the flag.
#but there is still way, let's keep track at the i th character of the flag.
#suppose we know the first i characters of the flag: f[0],f[1],...,f[i-1]
#we wish to know f[i], then insert (47-i) 1s before the flag, 
##now the padded string is PADDED1=11...1f[0]f[1]...f[i-1]f[i]...f[n], thus
#PADDED1[:48]=11...1f[0]f[1]...f[i-1]f[i] look at the first 3 blocks of 
#encrypt(PADDED1), call it RESULT1.
#Now brute force. We consider the string in the form 111.1f[0]f[1]...f[i-1]C
#where C runs over all possible characters, and the numbers of 1s is (47-i).
#now the padded string is PADDED2=11...1f[0]f[1]...f[i-1]Cf[0]f[1]...f[n], thus
# PADDED2[:48]=11..1f[0]f[1]...f[i-1]C 
#For each C, look at the result of the first 3 blocks of encrypt(PADDED2), 
#call it RESULT2.
#if RESULT1==RESULT2 then C=f[i]
#if C==} then we are done.



init=48-8
initstr='crypto{'
length=len(initstr)
while True:
    test=bytes.hex(b'1'*init)
    RESULT1=encrypt(test)[:96]
    for c in alphabet:
        m=b'1'*init+initstr.encode()+c.encode()
        test2=bytes.hex(m)
        RESULT2=encrypt(test2)[:96]
        if RESULT1==RESULT2:
            initstr+=c
            init-=1
            break
    if initstr[-1]=='}':
        break
print(initstr)
