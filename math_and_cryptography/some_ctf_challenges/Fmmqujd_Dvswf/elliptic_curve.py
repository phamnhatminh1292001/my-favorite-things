#!/usr/bin/env python3

def addition (p,q,prime,a,b):
    if p==[0,0]:
        return q
    elif q==[0,0]:
        return p
    elif p[0]==q[0] and p[1]==-q[1]:
        return 0
    else:
        lam=0
        if p!=q:
            temp=pow(q[0]-p[0],-1,prime)
            lam=((q[1]-p[1])*temp)%prime
        else:
            temp=pow(2*p[1],-1,prime)
            lam=((3*p[0]*p[0]+a)*temp)%prime
        c=lam*lam-p[0]-q[0]
        d=lam*(q[0]-c)-q[1]
        return [c%prime,d%prime]


def scalarmulti (p,n,prime,a,b):
    q=p
    r=[0,0]
    while n>0:
        if n%2==1:
            r=addition(r,q,prime,a,b)
        q=addition(q,q,prime,a,b)
        n=n//2
    return [r[0]%prime,r[1]%prime]
x=scalarmulti([2339, 2213],7863,9739, 497,1768)
print(x)