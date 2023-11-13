from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import math
from Crypto.Util.number import long_to_bytes
#just search Ron was wrong, Whit is right on google
#the paper is very long, but we just need the main words
#just read the 3 first pages, we can see that the problem is
#that some of the moduli has one same prime factor, say n1,n2
#since n1 and n2 have a prime factor p, this p is their gcd
Nlist=[]
elist=[]
clist=[]
for i in range(1,51):
    f=open(f"keys_and_messages/{i}.pem", 'r').read()
    key=RSA.import_key(f)
    Nlist.append(int(key.n))
    elist.append(int(key.e))
    f2=open(f"keys_and_messages/{i}.ciphertext", 'r').read()
    clist.append(int(f2,16))

found1=0
found2=0
vulnerable=[]
for i in range(0,len(Nlist)):
    for j in range(0,len(Nlist)):
        if j==i:
            continue
        gcd=math.gcd(Nlist[i],Nlist[j])
        if (gcd>1):
            print(gcd)
            q=Nlist[i]//gcd
            phi=(q-1)*(gcd-1)
            d=pow(elist[i],-1,phi)
            vulnerable.append((elist[i],d,clist[i],Nlist[i]))

for i in vulnerable:
    key = RSA.construct((i[3], i[0], i[1]))
    cipher = PKCS1_OAEP.new(key)
    decrypted=long_to_bytes(i[2])
    msg = cipher.decrypt(decrypted)
    if b"crypto" in msg:
        print(msg)

# references:
# https://eprint.iacr.org/2012/064.pdf
# https://www.slideshare.net/robertdallasgray/whos-right
# https://cryptanalysis.eu/blog/2012/04/06/ron-was-wrong-whit-is-right-weak-keys-in-the-internet/
