import itertools
import json
from hashlib import sha512
import pwn
import json

FLAG = "crypto{????????????????????????????????}"

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

class MyCipher:
    __NR = 31
    __SB = [13, 14, 0, 1, 5, 10, 7, 6, 11, 3, 9, 12, 15, 8, 2, 4]
    __SR = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]

    def __init__(self, key):
        self.__RK = int(key.hex(), 16)
        self.__subkeys = [[(self.__RK >> (16 * j + i)) & 1 for i in range(16)]
                          for j in range(self.__NR + 1)]

    def __xorAll(self, v):
        res = 0
        for x in v:
            res ^= x
        return res

    def encrypt(self, plaintext):
        assert len(plaintext) == 8, "Error: the plaintext must contains 64 bits."

        S = [int(_, 16) for _ in list(plaintext.hex())]

        for r in range(self.__NR):
            S = [S[i] ^ self.__subkeys[r][i] for i in range(16)]
            S = [self.__SB[S[self.__SR[i]]] for i in range(16)]
            X = [self.__xorAll(S[i:i + 4]) for i in range(0, 16, 4)]
            S = [X[c] ^ S[4 * c + r]
                 for c, r in itertools.product(range(4), range(4))]

        S = [S[i] ^ self.__subkeys[self.__NR][i] for i in range(16)]
        return bytes.fromhex("".join("{:x}".format(_) for _ in S))


class MyHash:
    def __init__(self, content):
        self.cipher = MyCipher(sha512(content).digest())
        self.h = b"\x00" * 8
        self._update(content)

    def _update(self, content):
        for i in range(0, len(content), 8):
            self.h = bytes(x ^ y for x, y in zip(self.h, content[i:i+8]))
            self.h = self.cipher.encrypt(self.h)
            self.h = bytes(x ^ y for x, y in zip(self.h, content[i:i+8]))

    def digest(self):
        return self.h

    def hexdigest(self):
        return self.h.hex()

lst=['6','7']
lst2=[]
for i in lst:
    for j in lst:
        lst2.append(i+j)
lst4=[]
for i in lst2:
    for j in lst2:
        lst4.append(i+j)
lst8=[]
for i in lst4:
    for j in lst4:
        lst8.append(i+j)
lst16=[]
for i in lst8:
    for j in lst8:
        lst16.append(i+j)
u=""
for i in lst16:
    for j in lst16:
        if MyHash(bytes.fromhex(i+j)).digest()==b"\x00"*8:
            u=i+j
            break
    if u !="":
        break
r=pwn.connect('socket.cryptohack.org',13393)
line=json_recv()
request={'option':'hash','data':u}
json_send(request)
line=json_recv()
print(line)