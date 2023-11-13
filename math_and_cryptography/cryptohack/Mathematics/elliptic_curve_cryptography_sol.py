from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
import hashlib 
import random
import os
from collections import namedtuple
from sympy.ntheory import factorint
import math
# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")
FLAG = b"crypto{????????????????????????????????}"  # REMOVE ME






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
    return a%((p-1)//2)


def point_addition(P, Q):
    Rx = (P.x*Q.x + D*P.y*Q.y) % p
    Ry = (P.x*Q.y + P.y*Q.x) % p
    return Point(Rx, Ry)


def scalar_multiplication(P, n):
    Q = Point(1, 0)
    while n > 0:
        if n % 2 == 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
        n = n//2
    return Q
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
# Curve parameters #
# ================ #

p = 173754216895752892448109692432341061254596347285717132408796456167143559 #congruent to 3 (mod 4)
D = 529 #this is a square
G = Point(29394812077144852405795385333766317269085018265469771684226884125940148,
          94108086667844986046802106544375316173742538919949485639896613738390948)
A=Point(x=155781055760279718382374741001148850818103179141959728567110540865590463, y=73794785561346677848810778233901832813072697504335306937799336126503714)
B=Point(x=171226959585314864221294077932510094779925634276949970785138593200069419, y=54353971839516652938533335476115503436865545966356461292708042305317630)
flag={'iv': '64bc75c8b38017e1397c46f85d4e332b', 'encrypted_flag': '13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf'}

#this is a Pell equation
#fortunately, the user make a fatal mistake by choosing a prime p such that p-1
#has only small primes

r1=(G.x+23*G.y)
r2=(G.x-23*G.y)


A1=A.x
B1=B.x
# c=r1^a, c^2+1=2Ac (mod p)
# (c-A)^2=A^2-1 (mod p)
#thus we can find r1^a
#now run Polig-Hellman algorithm to find a

a1=pow(A1**2-1,(p+1)//4,p)
c1=(a1+A1)%p
a=Po_He(r1,c1,p)

#similarly, we can find b
b1=pow(B1**2-1,(p+1)//4,p)
c2=(b1+B1)%p
b=Po_He(r1,c2,p)
shared=((pow(r1,a*b,p)+pow(r2,a*b,p))*pow(2,-1,p))%p

decrypted=decrypt_flag(shared,flag['iv'],flag['encrypted_flag'])
print(decrypted)
 









