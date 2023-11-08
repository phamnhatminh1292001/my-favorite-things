
from os import urandom
import json
from Crypto.Cipher import AES
from Crypto.Util.number import *
import pwn
from sage.all import *
import random
from sage.modules.free_module_integer import IntegerLattice
FLAG = 'crypto{??????????????????????}'

u = 8


class LCG:
    def __init__(self, a, b, m, seed):
        self.a = a
        self.b = b
        self.m = m
        self.state = seed
        self.counter = 0

    def refresh(self):
        self.counter = 0
        self.state = random.randint(1, 2**48)

    def next_state(self):
        self.state = (self.a * self.state + self.b) % self.m

    def get_random_bits(self, k):
        if self.counter == 16:
            self.refresh()
        self.counter += 1
        self.next_state()
        return (self.state >> (48 - k), self.state)

    def get_random_bytes(self, number):
        bytes_sequence = b''
        v2 = []
        for i in range(number):
            v = self.get_random_bits(8)
            bytes_sequence += long_to_bytes(v[0])
            v2 += [v[1]]
        return bytes_sequence, v2


def Babai_closest_vector(M, G, target):
    small = target
    for _ in range(1):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small


a = 0x1337deadbeef
b = 0xb
m = 2**48


def Babai_closest_vector(M, G, target):
    small = target
    for _ in range(1):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small


def solveLCG(d):
    v1 = [2**40*d[i]*a+b-2**40*d[i+1] for i in range(0, 7)]
    A1 = [pow(a, i, 2**48) for i in range(0, 8)]

    B1 = [0]
    for i in range(1, 8):
        sum = 0
        for j in range(0, i):
            sum = (sum+a**j*v1[i-1-j]) % (2**48)
        B1.append(sum)

    M = []
    M.append(A1)
    for i in range(0, 8):
        M.append([0]*i+[2**48]+[0]*(7-i))

    M = Matrix(M)
# M = M.LLL()
    lattice = IntegerLattice(M, lll_reduce=True)
    v = vector(B1)
    gram = lattice.reduced_basis.gram_schmidt()[0]
# print(gram)
    res = Babai_closest_vector(lattice.reduced_basis, gram, v)
# v = vector(ZZ, [0]*7+c+[-1])
# x = M.solve_left(v)
    return (v-res)


def json_recv():
    line = r.recvline()
    line = line.decode()
    return line


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


r = pwn.connect("socket.cryptohack.org", 13396)
r.recvline()
print(r)
ans = {"option": "get_a_challenge"}
json_send(ans)
line = json_recv()
line = json.loads(line)

print(line)
m = line['plaintext']

iv = line['IV']


d = [int(m[i:i+2], 16) for i in range(16, 32, 2)]

s1 = solveLCG(d)[7]
s1 = s1+2**40*d[7]
lst1 = []
key = b""
for i in range(0, 8):
    s1 = ((a*s1+b) % (2**48))
    lst1 = lst1+[s1 >> 40]
    key = key+long_to_bytes(s1)


d = [int(iv[i:i+2], 16) for i in range(0, 16, 2)]
s1 = solveLCG(d)[0]
s1 = s1+2**40*d[0]
lst2 = []
for i in range(0, 8):
    s1 = ((s1-b)*pow(a, -1, 2**48) % (2**48))
    lst2 = [s1 >> 40]+lst2
key = bytes(lst1+lst2)
print(key)
m = bytes.fromhex(m)
iv = bytes.fromhex(iv)
cipher = AES.new(key, AES.MODE_CBC, iv)
c = cipher.encrypt(m)
print(c)
ans = {"option": "validate", "ciphertext": c.hex()}
print(c.hex())
json_send(ans)
line = r.recvline()
print(line)
