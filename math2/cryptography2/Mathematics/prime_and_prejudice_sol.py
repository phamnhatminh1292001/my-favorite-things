#!/usr/bin/env python3

import math
from sympy import *
import telnetlib
import json
HOST = "socket.cryptohack.org"
PORT = 13385

FLAG = 'crypto{????????????????????????????????????}'


def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if basis[i]:
            basis[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]

#the idea is to find a Camichel number that will passes Miller-Rabin test from base 2 to base 64
#Initially, I intended to find an n with 2 prime number, but it was impossible since it could only
#pass the Fermat test. There is no way we could find an n with 2 prime factors that could pass the
#Miller Rabin test.
#Therefore we should find a number with exacly 3 prime factors. A paper of Arnault give a strategy to find a
#Camichel number with exacly 3 prime factors that could bypass the test
#It is believed that given a basis b, we can always find such an n, but it remains a conjecture.
#if we can find such a number n, then take a prime divisor p and assign p=a
#CRT function
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

# Generate all odd primes up to 64
basis=generate_basis(64)
basis.pop(0)
product=1
for i in basis:
    product=product*i

# for each odd prime up to 64, find the list of Non Quadratic Residues of the primes
def NQR(basis):
    dict={}
    for i in basis:
        dict[i]=[]
        for j in range(2,i):
            if pow(j,(i-1)//2,i)==(i-1):
                dict[i]+=[j]
    return dict
#generate the Non Quadratic Residues for all odd primes up to 64
dict=NQR(basis)

#these two functions help us find the smallest possible k2
def findNQR(p,k2):
    list=dict[p]
    for i in range(1,p):
        if (i in list) and ((67*i-66)%p in list) and ((k2*i-k2+1)%p in list):
            return True
    return False

def findk2(k2):
    found=False
    while (found==False):
        if not(isprime(k2)):
            k2+=2
            continue
        found2=True
        for i in basis:
            if findNQR(i,k2)==False:
                found2=False
                break
        if found2==True:
            break
        k2+=2                  
    return k2

# we have found the smallest possible k2. Now for each prime p, look for an i such that i, 67*i-66
# and k2*i-k2+1 are all Non Quadratic Residues mod p, then append i for CRT
def appendforCRT(k2):
    list=[]
    for i in basis:
        for j in range(1,i):
            if (j in dict[i]) and ((67*j-66)%i in dict[i]) and ((k2*j-k2+1)%i in dict[i]):
                list.append(j)
                break
    return list

# we found that k2=127
x=127
list2=appendforCRT(x)

#we need 67p+1=0(mod 127) and 127p+1=0(mod 67) and p=5(mod 8)
t1=127-pow(67,-1,127)             
e1=127
t2=67-pow(127,-1,67)
e2=67           
t3=5
e3=8
list2+=[t1,t2,t3]
basis+=[e1,e2,e3]
#now call the CRT function to find p
p=CRT(basis,list2)
a=p[0]
b=p[1]
t=2**200//b
a=a+t*b
#now just do the while loop until we found such a p
boolean1=isprime(a)
boolean2=isprime(67*a-66)
boolean3=isprime(127*a-126)
while boolean1==False or boolean2==False or boolean3==False:
    a+=b
    boolean1=isprime(a)
    boolean2=isprime(67*a-66)
    boolean3=isprime(127*a-126)
n=a*(67*a-66)*(127*a-126)

#now victory is at hand

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

q=readline().decode()
request={'prime':n,'base':a}
json_send(request)
q=readline().decode()
print(q)

#Reference: Fran¸cois Arnault. Constructing Carmichael numbers which are strong pseudoprimes to several
#bases. Journal of Symbolic Computation, 20(2):151–161, 1995.


