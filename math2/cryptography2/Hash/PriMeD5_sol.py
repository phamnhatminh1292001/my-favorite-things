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
# the output of MD5 is given as follow, let s[1] be the initital state. Then the states s[2],...s[k]
# is generated recursively by having s[i+1]=f(s[i],m[i]) where f is a fixed function. MD5 outputs s[k]
# from above, we see that a fatal weakness of MD5 is that, given two byte strings having the same 
# hash value, say m1 and m2,  we can insert any byte strings with length divisible by 16  
# behind m1 and m2, and the two new strings still have the same hash value. We will use this to  
# modify m1 and m2 to receive a prime number and a composite number
a=int(m1,16)
b=int(m2,16)
t=2**512
c=t*a
a=t*a
b=t*b
r=61-b%61
a=a+r
b=b+r
#we will insert a block behind a and b such that a is a prime and b is a composite
#if the block is m bits behind a, then the number obtained has the following form:
#2^m*a+r for some r<2^m, thus, fix an m, we will try r from 1 to 2^m to find a r such
#that 2^m*a+r is a prime and 2^m*b+r is a composite, we let m=512 (since 1 byte=8 bit
#and the length of a byte string is divisible by 64, thus m is divisible by 64*8=512)
#we will also try those r so that 2^m*b+r is divisible by 61
c=t*a+2**512
while a<c:
    if (isPrime(a)) and (not isPrime(b)):
        break
    a=a+61
    b=b+61
#since b is divisible by 61, we will choose 61 to force the server to reveal the flag
c=61
prime1=str(a)
prime2=str(b)
r=pwn.connect('socket.cryptohack.org',13392)
json_recv()
request={'option':'sign','prime':prime1}
json_send(request)
line=json_recv()
s=take_dict(line)
sign=s['signature']
request={'option':'check','prime':prime2,'signature':sign,'a':c}
json_send(request)
print(json_recv())
#reference: https://www.mscs.dal.ca/~selinger/md5collision/
