from sympy import isprime
import re
import numpy as np

#integer overflow in numpy


def check(password):
    if not re.fullmatch(r"\w*", password, flags=re.ASCII):
        return "Password contains invalid characters."
    if not re.search(r"\d", password):
        return "Password should have at least one digit."
    if not re.search(r"[A-Z]", password):
        return "Password should have at least one upper case letter."
    if not re.search(r"[a-z]", password):
        return "Password should have at least one lower case letter."

    array = np.array(list(map(ord, password)))
    if isprime(int(array.sum())) and isprime(int(array.prod())):
        return "YES"
    else:
        return f"Wrong password, sum was {array.sum()} and product was {array.prod()}"


#we will brute force and stop when we found a string

for i in range(49,127):
    for j in range(49,127):
        for k in range (49,127):
            for l in range (49,127):
                array=chr(i)+chr(j)+chr(k)+chr(l)+chr(65)+chr(121)*6
                if check(array)=="YES":
                    print(array)

#well, since we have 4 for loops, which is enough  to brute force
#we receive a string "1iIiAyyyyyy" which passes the check condition
#and of course, if we find the string, we will stop the program
#and continue the next step, since the the for loops will run forever
#if we don't stop.

import json
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

r=pwn.connect('socket.cryptohack.org',13400)
json_recv()

request={"password":"1iIiAyyyyyy"}
json_send(request)
line=json_recv()
print(line)
