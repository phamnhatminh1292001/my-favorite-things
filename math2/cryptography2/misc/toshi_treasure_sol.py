
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
M=2 ** 521 - 1
r=pwn.connect('socket.cryptohack.org',13384) 
line=json_recv()
print(line)
s=take_dict(line)
y=int(s['y'],16)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
msg={'x':6,'y':"0x00"}
json_send(msg)
line=json_recv()
print(line)
s=take_dict(line)
fake0=s['privkey']
my_basis=(2*3*4*5*pow((2-6)*(3-6)*(4-6)*(5-6),-1,M))%M
line=json_recv()
print(line)
line=json_recv()
print(line)
my_1k_wallet_privkey = "8b09cfc4696b91a1cc43372ac66ca36556a41499b495f28cc7ab193e32eadd30"
my_fake_y=((int(my_1k_wallet_privkey,16)-int(fake0,16))*pow(my_basis,-1,M))%M
msg={'x':6,'y':hex(my_fake_y)}
json_send(msg)
line=json_recv()
print(line)
line=json_recv()
print(line)
line=json_recv()
print(line)
truekey=hex((int(fake0,16)+my_basis*y)%M)
msg={'privkey':truekey}
json_send(msg)
line=json_recv()
print(line)