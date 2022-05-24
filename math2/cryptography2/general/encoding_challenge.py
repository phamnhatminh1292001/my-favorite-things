from Crypto.Util.number import bytes_to_long, long_to_bytes 
import base64
import codecs
import random
import json
import telnetlib
def decode_level(encoding,challenge_words):

        if encoding == "base64":
            decoded = base64.b64decode(challenge_words).decode('utf8').replace("'", '"') # wow so encode
        elif encoding == "hex":
            decoded = bytes.fromhex(challenge_words).decode()
        elif encoding == "rot13":
            decoded = codecs.decode(challenge_words, 'rot_13')
        elif encoding == "bigint":
            challenge_words=int(challenge_words,16)
            decoded = long_to_bytes(challenge_words).decode()
        elif encoding == "utf-8":
            decoded=""
            for i in challenge_words:
                encoded+=chr(i)
        return {"type": encoding, "decoded": decoded}

HOST = "socket.cryptohack.org"
PORT = 13377


pr = telnetlib.Telnet(HOST, PORT)

def readline():
    return pr.read_until(b"\n")

def json_send(hsh):
    request = json.dumps(hsh).encode()
    pr.write(request)


def json_recv():
    line = readline()
    return json.loads(line.decode())

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
    str=json.loads(str)
    return str

for i in range(0,100):
    q=readline().decode()
    s=take_dict(q)
    type=s["type"]
    challenge_words=s["encoded"]
    request={"decoded":decode_level(type,challenge_words)['decoded']}
    json_send(request)

q=readline()
print(q)
