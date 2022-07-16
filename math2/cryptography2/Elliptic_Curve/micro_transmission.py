

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

a=1
b=4
p=99061670249353652702595159229088680425828208953931838069069584252923270946291
E = EllipticCurve(GF(p), [a,b])

G=E(43190960452218023575787899214023014938926631792651638044680168600989609069200, 20971936269255296908588589778128791635639992476076894152303569022736123671173)

Ax=87360200456784002948566700858113190957688355783112995047798140117594305287669
Ca=(Ax^3+a*Ax+b)%p
Ay= GF(p)(Ca).square_root()
Bx=6082896373499126624029343293750138460137531774473450341235217699497602895121
Cb=(Bx^3+a*Bx+b)%p
By = GF(p)(Cb).square_root()

A=E(Ax,-Ay)
B=E(Bx,-By)

print(A)
print(B)

n=E.order()

lst=[7 ,11 , 17 ,191 ,317 ,331 ,5221385621, 5397618469, 210071842937040101,637807437018177170959577732683]
lst2=[int(n)//int(i) for i in lst]
lst3=[]

for i in range(0,8):
    d=(lst2[i]*G).discrete_log(lst2[i]*B)
    lst3.append(d)
    
    
lst4=[7 ,11 , 17 ,191 ,317 ,331 ,5221385621,5397618469]
b1=crt(lst3,lst4)
print(b1)
s=A*b1
print(s)

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


s=92209717447332837440641806732517921920015580446111641942522142444036785043977
iv='ceb34a8c174d77136455971f08641cc5'
enc='b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453'

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