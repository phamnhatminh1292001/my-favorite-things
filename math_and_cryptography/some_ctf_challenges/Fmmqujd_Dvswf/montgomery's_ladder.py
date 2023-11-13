

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

A= 486662
def add(P,Q,p):
    alpha=((Q[1]-P[1])*pow(Q[0]-P[0],-1,p))%p
    x3=(alpha**2-A-P[0]-Q[0])%p
    y3=(alpha*(P[0]-x3)-P[1])%p
    return [x3,y3]

def double(P,p):
    alpha=((3*P[0]**2+2*A*P[0]+1)*pow(2*P[1],-1,p))%p
    x3=(alpha**2-A-2*P[0])%p
    y3=(alpha*(P[0]-x3)-P[1])%p
    return [x3,y3]

def mul(n,P,p):
    n=int(n,16)
    bi=[]
    while(n>0):
        if n%2==0:
            bi.append(0)
        else:
            bi.append(1)
        n=n//2
    R0=P
    R1=double(P,p)
    for i in range (len(bi)-2,-1,-1):
        if bi[i]==0:
            T0=double(R0,p)
            T1=add(R0,R1,p)
            R0=T0
            R1=T1
        else:
            T0=add(R0,R1,p)
            T1=double(R1,p)
            R0=T0
            R1=T1
    return R0

p=2**255-19
x=9
y=14781619447589544791020593568409986887264606134616475288964881837755586237401
R=mul("0x1337c0decafe",[x,y],p)
print(R)