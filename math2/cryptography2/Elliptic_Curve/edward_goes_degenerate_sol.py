from Crypto.Util.number import inverse, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
import hashlib 
import math
from sympy import*

FLAG = b'crypto{????????????????????????????????????}'


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
        #it is easy to see gamma^a[i]=d[i] (mod p), thus we can compute a[i]
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



# curve parameters
# birationally equivalent to the Montgomery curve y**2 = x**3 + 337*x**2 + x mod p
p = 110791754886372871786646216601736686131457908663834453133932404548926481065303
orx = 27697938721593217946661554150434171532902064063497989437820057596877054011573
d = 14053231445764110580607042223819107680391416143200240368020924470807783733946

y0 = 11
yA=109790246752332785586117900442206937983841168568097606235725839233151034058387
yB=45290526009220141417047094490842138744068991614521518736097631206718264930032
a=Po_He(y0,yA,p)
b=Po_He(y0,yB,p)
shared=pow(yB,a,p)

iv='31068e75b880bece9686243fa4dc67d0'
enc='e2ef82f2cde7d44e9f9810b34acc885891dad8118c1d9a07801639be0629b186dc8a192529703b2c947c20c4fe5ff2c8'
d=decrypt_flag(shared,iv,enc)
print(d)

