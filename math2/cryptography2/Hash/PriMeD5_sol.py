import itertools
import json
from hashlib import sha512
from Crypto.Util.number import bytes_to_long, long_to_bytes, isPrime
from Crypto.Hash import MD5
import pwn
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
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

m1='4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2'
m2='4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2'
# how MD5 works: given a byte string m, it will be divided into 16 byte strings m[1],m[2],...m[k]
# the output of MD5 is a string s=s[1]s[2]...s[k] and each character is obtained
# recursively by having s[i+1]=f(s[i],m[i]) where f is a fixed function
# from above, we see that a fatal weakness of MD5 is that, given two byte strings having the same 
# hash value, say m1 and m2,  we can insert any byte strings with length divisible by 16  
# behind m1 and m2, and the two new strings still have the same hash value. We will use this to  
# modify m1 and m2 to receive a prime number and a composite number
a=int(m1,16)
b=int(m2,16)
t=2**128
c=t*a
a=t*a+1
b=t*b+1
#we will insert a block behind a and b such that a is a prime and b is a composite
#if the block is m bits behind a, then the number obtained has the following form:
#2^m*a+r for some r<2^m, thus, fix an m, we will try r from 1 to 2^m to find a r such
#that 2^m*a+r is a prime and 2^m*b+r is a composite, m is a multiple of 128 (since 1 byte=8 bit
#and the length of a byte string is divisible by 16, thus m is divisible by 16*8=128)
#we will try small a and b first because we want to factorize b, it is not good if
#b is big
c=t*a+2**128
while a<c:
    if (isPrime(a)) and (not isPrime(b)):
        break
    if a%6==1:
        a+=4
        b+=4
    else:
        a+=2
        b+=2
#one factor of b
#use factordb to obtain c
c=6631140029601908490133118510209548000474184326629465829835060199270556279877111825662877532337461468379264783850607195857415101062007439555851252562345132207315279
prime1=str(a)
prime2=str(b)
r=pwn.connect('socket.cryptohack.org',13392)
json_recv()
request={'option':'sign','prime':prime1}
json_send(request)
line=json_recv()
print(line)
s=take_dict(line)
sign=s['signature']
request={'option':'check','prime':prime2,'signature':sign,'a':c}
json_send(request)
print(json_recv())
#reference: https://www.mscs.dal.ca/~selinger/md5collision/