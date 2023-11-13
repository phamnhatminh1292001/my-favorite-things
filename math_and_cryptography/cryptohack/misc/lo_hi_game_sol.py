from functools import total_ordering
from Crypto.Random import random
import json
from hashlib import sha512
from Crypto.Util.number import bytes_to_long, long_to_bytes, isPrime
import pwn

VALUES = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six',
          'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
SUITS = ['Clubs', 'Hearts', 'Diamonds', 'Spades']


t=[f"{value} of {suit}" for suit in SUITS for value in VALUES]

def rebase(n, b=52):
        if n < b:
            return [n]
        else:
            return [n % b] + rebase(n//b, b)


def getnum(str):
    str=take_dict(str)
    get=str['hand']
    idx=t.index(get)
    return idx


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


def guess():
    global num
    global round
    request={'choice':'l'}
    json_send(request)
    line=json_recv()
    print(line)
    z=getnum(line)
    num=52*num+z
    round+=1
    return take_dict(line)['hand']

def cheat(value,g):
    global round 
    str=t[value].split(" ")[0]
    g=g.split(" ")[0]
    idx1=VALUES.index(g)
    idx2=VALUES.index(str)
    if idx1>idx2:
        request={'choice':'l'}
        json_send(request)
    else:
        request={'choice':'h'}
        json_send(request)
    line=json_recv()
    print(line)
    round+=1
    s=take_dict(line)['hand']
    print(t.index(s))
    return take_dict(line)['hand']




r=pwn.connect('socket.cryptohack.org',13383)
num=0
line=json_recv()
print(line)
z=getnum(line)
num=52*num+z
round=1
g=""
X1=0
X2=0
X3=0
M=2**61-1
X=0
while round<201:
    #since I am lazy, I will just play until all the first three random
    #numbers have 11 digits in base 52, in other words all of c%M, (ac+b)%M
    #and (a(ac+b)+b)%M must have 11 digits in base 52
    if round<11:
        g=guess()
    #get the c%m, only works if c%M has 11 digits in base 52  
    elif round==11:
        X1=num
        num=0
        g=guess()
    #get the (ac+b)%m, only works if (ac+b)%M has 11 digits in base 52 
    elif round<22:
        g=guess()
    elif round==22:
        X2=num
        num=0
        g=guess()
    #get the (a(ac+b)+b)%m, only works if (ac+b)%M has 11 digits in base 52 
    #if we can go to this phrase, then victory is at hand.
    elif round<33:
        g=guess()
    elif round==33:
        X3=num
        A=((X3-X2)*(pow((X2-X1),-1,M)))%M
        B=(X2-A*X1)%(M)
        X=(A*X3+B)%(M)
        lst=rebase(X,52)
        print(lst)
        g=cheat(lst[len(lst)-1],g)
        lst.pop()
    elif lst!=[]:
        g=cheat(lst[len(lst)-1],g)
        lst.pop()
    else:
        X=(A*X+B)%(M)
        lst=rebase(X,52)
        g=cheat(lst[len(lst)-1],g)
        lst.pop()