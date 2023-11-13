from ftplib import parse150
from unicodedata import decimal
import pwn
import json
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, getPrime
from gmpy2 import mpz
from Crypto.Util.Padding import pad, unpad
import hashlib
from sympy import *
import math
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

def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if basis[i]:
            basis[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]

def order(m,p):
    dict=factorint(p-1)
    product=1
    for i in dict:
        e=1
        test=pow(m,(p-1)//(i**e),p)
        while test==1:
            e+=1
            if e==dict[i]+1:
                break
            test=pow(m,(p-1)//(i**e),p)
        product=product*(i**(dict[i]-e+1))
    return product 

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
    ord=order(g,p)
    c=factorint(ord)
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
        b=(product//i)*pow(product//i,-1,i)%(ord)
        list3+=[b]
    a=0
    for i in range(0,len(list)):
        a+=list2[i]*list3[i]%(ord)
    return a%ord  










# we will create a product of A LOT of smooth primes
list=generate_basis(200)
list.pop(0)
compare=2**50
product=1
for i in range(0,len(list)):
    p=list[i]
    while(list[i]*p<compare):
        list[i]=list[i]*p
    product=product*list[i]
product=product*2



j=1+product
bitprime=j.bit_length()
while bitprime<4000:
    while not(isprime(j)):
        j+=4*product
    bitprime=j.bit_length()
    ord=order(2,j)
    bitord=ord.bit_length()
    if bitord>1500:
        break
    j+=4*product

r = pwn.connect('socket.cryptohack.org', 13378)
q=json_recv()
p=q['p']
A=q['A']
g=q['g']
q=json_recv()
B=q['B']
q=json_recv()
iv1=q['iv']
encrypted=q['encrypted']
request={'p':hex(j),'g':g,'A':'0x04'}
json_send(request)
q=json_recv()
B2=int(q['B'],16)
b=Po_He(2,B2,j)

A=int(A,16)
p=int(p,16)
print(p.bit_length())
shared=pow(A,b,p)
decrypted=decrypt_flag(shared,iv1,encrypted)
print(decrypted)
