from unicodedata import decimal
import pwn
import telnetlib
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
import hashlib
import sympy
from sympy.ntheory import factorint
HOST = "socket.cryptohack.org"
PORT = 13379
import math

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

def Po_He_prime(g,q,n,p):
    N = 1 + int(math.sqrt(q))

    #initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * g % p

    #now take the giant steps
    giant_stride = pow(g,(p-2)*N,p)
    giant_step = n
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
    return "No Match"

def Po_He_prime_power(g,q,e,n,p):
    gamma=pow(g,q**(e-1),p)
    #the main idea is to compute x[e]=a[0]+a[1]*q+a[2]*q^2+...+a[e-1]*q^(e-1)
    # we compute x[i]=a[0]+a[1]*q+a[2]+q^2+...+a[i-1]*q^(i-1) and return x[e]
    x=0
    for i in range(0,e):
        #compute d[i]=(g^(-x[i])*h)^(q-1-i)
        t1=pow(g,q**e-x,p)
        d=pow((t1*n),q**(e-1-i),p)
        a=Po_He_prime(gamma,q,d,p)
        #it is easy to see gamma^a[i]=d[i] (mod p)
        x=x+(q**i)*a
    return x

def Po_He(g,n,p):
    c=factorint((p-1)//2)
    list=[]
    list2=[]
    product=1
    for i in c:
        a=pow(i,c[i])
        list+=[a]
        product=product*a
    count=0
    for i in c:
        g2=pow(g,product//list[count],p)
        n2=pow(n,product//list[count],p)
        list2+=[Po_He_prime_power(g2,i,c[i],n2,p)]
        count+=1    
    list3=[]
    for i in list:
        b=(product//i)*pow(product//i,-1,i)%((p-1)//2)
        list3+=[b]
    a=0
    for i in range(0,len(list)):
        a+=list2[i]*list3[i]%((p-1)//2)
    return a



q=readline().decode()
s=take_dict(q)
# DHi meaning Alice and Bob choose a prime with i bit. We prefer the smallest prime possible
supported="DH64"
request={"supported":["DH64"]}
json_send(request)
q=readline().decode()
s=take_dict(q)
request={"chosen":supported}
json_send(request)
q=readline().decode()
s=take_dict(q)
p=s['p']
g=s['g']
A=s['A']
request={'p':p,'g':g,'A':A}
json_send(request)
q=readline().decode()
s=take_dict(q)
B=s['B']
request={'B':B}
json_send(request)
q=readline().decode()
s=take_dict(q)
iv1=s['iv']
encrypted_flag1=s['encrypted_flag']
#Since p is small enough, it is possible to find a using Pohlig-Hellman algorithm
g=int(g,16)
B=int(B,16)
p=int(p,16)
A=int(A,16)
#use the algorithm to find a
a=Po_He(g,A,p)
key=pow(B,a,p)
m=decrypt_flag(key,iv1,encrypted_flag1)
print(m)


