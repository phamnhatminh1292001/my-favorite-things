
import pwn
import json
import hashlib
import time
from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
#this time, I decided to do pwn instead of telnetlib





def json_recv():
    line = r.recvline()
    line=line.decode()
    return line

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()


def xor(b,k):
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ k[i]])
    return ciphertext.hex()

r = pwn.connect('socket.cryptohack.org', 13372)
json_recv()
request={'option':'get_flag'}
data='00000000000000000000000000000000000000000000000000000000'
json_send(request)
flag=json.loads(json_recv())['encrypted_flag']
request={'option':'encrypt_data','input_data':data}
json_send(request)
data2=json.loads(json_recv())['encrypted_data']
flag=bytes.fromhex(flag)
data2=bytes.fromhex(data2)
xorresult=bytes.fromhex(xor(data2,flag))
print(xorresult)


