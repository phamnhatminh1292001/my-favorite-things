from Crypto.Random import random
from Crypto.Util.number import getPrime, bytes_to_long

FLAG = b'crypto{??????????????????????????????????????????}'

def get_padding():
    seed = 256
    e = random.randint(2, q)
    padding = pow(seed, e, q)
    return padding


def public_key():
    x = random.randint(2, q)
    return pow(g, x, q)


def encrypt(m, h):
    y = random.randint(2, q)
    s = pow(h, y, q)
    c1 = pow(g, y, q)
    c2 = (s * m) % q
    return (c1, c2)

m = bytes_to_long(FLAG)
while m:
    padding = get_padding()
    #WARNING: + IS DONE BEFORE <<, THUS
    #me=padding*2^(1+m%2), NOT me=2*padding+m%2
    me = padding << 1 + m % 2
    h = public_key()
    (c1, c2) = encrypt(me, h)
    print(f'(public_key={hex(h)})')
    print(f'(c1={hex(c1)}, c2={hex(c2)})')
    m //= 2

q = 117477667918738952579183719876352811442282667176975299658506388983916794266542270944999203435163206062215810775822922421123910464455461286519153688505926472313006014806485076205663018026742480181999336912300022514436004673587192018846621666145334296696433207116469994110066128730623149834083870252895489152123
g = 104831378861792918406603185872102963672377675787070244288476520132867186367073243128721932355048896327567834691503031058630891431160772435946803430038048387919820523845278192892527138537973452950296897433212693740878617106403233353998322359462259883977147097970627584785653515124418036488904398507208057206926

#note that c2[i]=g^(xy)*2*(256^e) (mod q) or  c2[i]=g^(xy)*4*(256^e) (mod q)
#we need to find when 2 and when 4, then we can get m[i]
#look at the difference is that 2 is a prime and 4 is a square and the number 256, 
#it is natural to consider QR, since we consider QR, we can see that g is a QR too
#and 2 is a NQR
#thus m[i]=1 iff (c2/q)=1
for i in range(0,(q-1//8)):
    s=(2*pow(256,i,q)+1)%q
    print(pow(s,(q-1)//2,q))
f=open(f"output.txt", 'r').read()
f=f.split('\n')
c2list=[]
for i in range(1,len(f)-1,2):
    x=f[i]
    x=x.split(" ")
    c2list.append(int(x[1][3:-1],16))
c2list.reverse()
mlist=[0]*len(FLAG)*8
mlist2=[]
for i in range(0,len(c2list)):
    if pow(c2list[i],(q-1)//2,q)==1:
        mlist[i+1]=1
#now we have found all i such that m[i]=1 by looking at (c2/q), the rest is decrypt
for i in range(0,len(mlist),8):
    mlist2.append(mlist[i:i+8])
s=''
for i in mlist2:
    s+=chr(i[7]+i[6]*2+i[5]*4+i[4]*8+i[3]*16+i[2]*32+i[1]*64+i[0]*128)
print(s)
