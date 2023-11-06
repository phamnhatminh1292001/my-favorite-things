import pwn
import json

from sage.all import *


charlist = []
for i in range(48, 58):
    if i % 8 == 1 or i % 8 == 5:
        charlist.append(i)
for i in range(65, 91):
    if i % 8 == 1 or i % 8 == 5:
        charlist.append(i)
for i in range(97, 123):
    if i % 8 == 1 or i % 8 == 5:
        charlist.append(i)
a = mod(5, 2 ^ 64)

dloglist = []
for i in range(0, len(charlist)):
    b = mod(charlist[i], 2 ^ 64)
    c = b.log(a)
    dloglist.append(c)

P = Primes()
primelist = []
for i in range(30, 6600):
    if P.unrank(i) % 8 == 1 or P.unrank(i) % 8 == 5:
        primelist.append(P.unrank(i))
dlogplist = []

for i in range(0, len(primelist)):
    b = mod(primelist[i], 2 ^ 64)
    c = b.log(a)
    dlogplist.append(c)


for i in range(0, len(primelist)):
    M = []
    for j in range(0, len(charlist)):
        X = [charlist[j]]+[dloglist[j]]+[0]*j+[1]+[0]*(len(charlist)-j)
        M.append(X)
    M.append([primelist[i]]+[dlogplist[i]]+[0]*len(charlist)+[1])
    M.append([0]+[2 ^ 62]+[0]*(len(charlist)+1))
    M = Matrix(ZZ, M)
    M2 = M.LLL()
    for t in range(0, 19):
        if (M2[t, 0] == 0) and (M2[t, 1] == 0) and (M2[t, 19] == 1 or M2[t, 19] == -1):
            print(M2[t])
            print(".........")
v = [0, 0, -1, -7, -4, -6, -14, -14, -4, -6, -
     23, -15, -11, -15, -16, -16, -19, -12, -26, 1]


sum = 0
for i in range(0, len(charlist)):
    sum = sum+charlist[i]*(-v[i+2])
print(sum)
mul = 1
for i in range(0, len(charlist)):
    mul = mul*pow(charlist[i], (-v[i+2]), 2 ^ 64) % 2 ^ 64
print(mul)
t = ''
for i in range(0, len(charlist)):
    t = t+chr(charlist[i])*(-v[i+2])
print(t)

t = '155555559999AAAAAAEEEEEEEEEEEEEEIIIIIIIIIIIIIIMMMMQQQQQQUUUUUUUUUUUUUUUUUUUUUUUYYYYYYYYYYYYYYYaaaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiiiiimmmmmmmmmmmmmmmmqqqqqqqqqqqqqqqqqqquuuuuuuuuuuuyyyyyyyyyyyyyyyyyyyyyyyyyy'
r = pwn.connect('socket.cryptohack.org',)
