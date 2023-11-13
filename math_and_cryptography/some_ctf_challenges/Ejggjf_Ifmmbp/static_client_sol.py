from ftplib import parse150
from unicodedata import decimal
import pwn
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
import hashlib
#this time, I decided to do pwn instead of telnetlib



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
    s=take_dict(line)
    return s

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

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

def CRT(list,list2):
    product=1
    list3=[]
    for i in list:
        product*=i
    for i in range(0,len(list)):
        c=product//list[i]
        inv=pow(c,-1,list[i])
        c=(c*inv)%product
        list3+=[c]
    CRT=0
    for i in range(0,len(list)):
        CRT+=(list3[i]*list2[i])%product
    return (CRT%product,product)



arr1=[]
arr2=[]
for i in range(0,2):
    r = pwn.connect('socket.cryptohack.org', 13373)
    q=json_recv()
    p=q['p']
    A=q['A']
    g=q['g']
    q=json_recv()
    B=q['B']
    q=json_recv()
    iv1=q['iv']
    encrypted=q['encrypted']

    p1=getPrime(1024)
    arr1.append(p1)
    g=hex(p1+1)
    p2=hex(p1*p1)
    request={'p':p2,'g':g,'A':'0x1'}
    json_send(request)
    q=json_recv()
    B2=int(q['B'],16)
    b=(B2-1)//p1
    arr2.append(b)


b=CRT(arr1,arr2)[0]
shared=pow(int(A,16),b,int(p,16))
decrypted=decrypt_flag(shared,iv1,encrypted)
print(decrypted)
