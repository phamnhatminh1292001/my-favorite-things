import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def addition (p,q,prime,a,b):
    if p==[0,0]:
        return q
    elif q==[0,0]:
        return p
    elif p[0]==q[0] and p[1]==-q[1]:
        return 0
    else:
        lam=0
        if p!=q:
            temp=pow(q[0]-p[0],-1,prime)
            lam=((q[1]-p[1])*temp)%prime
        else:
            temp=pow(2*p[1],-1,prime)
            lam=((3*p[0]*p[0]+a)*temp)%prime
        c=lam*lam-p[0]-q[0]
        d=lam*(q[0]-c)-q[1]
        return [c%prime,d%prime]


def scalarmulti (p,n,prime,a,b):
    q=p
    r=[0,0]
    while n>0:
        if n%2==1:
            r=addition(r,q,prime,a,b)
        q=addition(q,q,prime,a,b)
        n=n//2
    return [r[0]%prime,r[1]%prime]

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

p=9739
pointx=4726
mod=(pow(pointx,3)+497*pointx+1768)%p
pointy1=pow(mod,(p+1)//4,p)
point=[pointx,pointy1]
x=scalarmulti(point,6534,p, 497,1768)

shared_secret = x[0]
iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

print(decrypt_flag(shared_secret, iv, ciphertext))
