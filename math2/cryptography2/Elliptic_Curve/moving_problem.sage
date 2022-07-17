

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad





p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a,b])
G=E(479691812266187139164535778017,568535594075310466177352868412)
A=E(1110072782478160369250829345256,800079550745409318906383650948)
B=E(1290982289093010194550717223760,762857612860564354370535420319)
n=E.order()
k=2
#now consider the Field GF(p^k)
K.<a> = GF(p^k)
#extend from E(GF(p)) to E(GF(p^k))
EK = E.base_extend(K)
AK = EK(A)
GK = EK(G)
#generate a random point
Qk = EK.random_point()
m = Qk.order()
d = gcd(m, G.order())
Qk = (m//d)*Qk
#weil's pairing
AA = AK.weil_pairing(Qk, n)
GG = GK.weil_pairing(Qk, n)
print(AA)
print(GG)
u=discrete_log(AA,GG)
print(u)
S=B*u
print(S)


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))
s=57514367079882430785803122958
iv='eac58c26203c04f68d63dc2c58d79aca'
enc='bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'
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
print(decrypt_flag(s, iv, enc))
