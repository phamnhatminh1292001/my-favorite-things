
import pwn
import json


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


#this part is done in Sage
#set up the curve secp256r1
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
K = GF(p)
a = K(0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc)
b = K(0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b)
E = EllipticCurve(K, (a, b))
G=2*E(0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531, 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A)
print(G.xy())
n=Integer(E.order())
d=pow(2,-1,n)
print(d)

#this part is done in python
r=pwn.connect('socket.cryptohack.org',13382)
line=json_recv()
request={
    "curve": "secp256r1",
    "host":"www.bing.com",
    "generator":[41356219197037336402569455855811057698565586129318592577359663831246482999742, 46303690855896669118039560713730632567800729889406997568787293237676888679144],
    "private_key":57896044605178124381348723474703786764998477612067880171211129530534256022185
}
json_send(request)
line=json_recv()
print(line)