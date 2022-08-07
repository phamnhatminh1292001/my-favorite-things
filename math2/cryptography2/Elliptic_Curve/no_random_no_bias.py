from hashlib import sha1
G=(48439561293906451759052585252797914202762949526041747995844080717082404635286,36134250956749795798585127919587881956611106672985015071877198253568414405109)
msg1='I have hidden the secret flag as a point of an elliptic curve using my private key.'
msg2='The discrete logarithm problem is very hard to solve, so it will remain a secret forever.'
msg3='Good luck!'
hsh1=int(sha1(msg1.encode()).digest().hex(),16)
hsh2=int(sha1(msg2.encode()).digest().hex(),16)
hsh3=int(sha1(msg3.encode()).digest().hex(),16)
hsh=[hsh1,hsh2,hsh3]
r=[0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae,0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c,0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6]
s=[0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d,0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8,0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba]
n=115792089210356248762697446949407573529996955224135760342422259061068512044369
#s=(hsh+r*d)/k (mod n) => k=(hsh+r*d)/s (mod n)
#k[0]=b[0]+d*a[0]+n*t[0]
#k[1]=b[1]+d*a[1]+n*t[1]
#k[2]=b[2]+d*a[2]+n*t[2]
b=[]
a=[]
for i in range(0,3):
    b.append(Integer(hsh[i]*pow(s[i],-1,n)%n))
for i in range(0,3):
    a.append(Integer(r[i]*pow(s[i],-1,n)%n))
    
M=Matrix(QQ,5,5)
for i in range(0,3):
    M[i,i]=n
for i in range (0,3):
    M[3,i]=a[i]
for i in range (0,3):
    M[4,i]=b[i]

M[3,3]=2^160/n
M[4,4]=2^160
N=M.LLL()
print(N)
#checking the firt row, only the second entry has value less than 2^160, so it has a high chance to be the first nonce, so we look for the second column
#and the last entry of the second row is equal to 2^160, thus this is exacly the correct column
t=2^160
#we have that the fourth entry of the second column should be d*n/(2^160), but for some reason it has negative value, fortunately it is because the LLL matrix
#returns (d-n)*M[3] instead of d*M[3], but anyway, let's check if it is correct
d=N[1,3]*n/t+n
print(d)

p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
E = EllipticCurve(GF(p), [a, b])
T= E(16807196250009982482930925323199249441776811719221084165690521045921016398804,72892323560996016030675756815328265928288098939353836408589138718802282948311)
inv=pow(Integer(d),-1,n)
Q=T*inv
print(Q)
  
                                                                                                                                                 3389001176200954606976789504592874264927983410587162     ,                                                                                                                                                      2402123901147245112784294079764879681480493880673541           ,                                                                                                                                                 927358714641904682627771297291682648578280222599381 ,  90498734917360654896771677717033300102042233684563159671095345718388240142432443338846831937728591587547403376123381645574144/115792089210356248762697446949407573529996955224135760342422259061068512044369      ,                                                                                                                                                    -1555037742120080704968720662010125132913912225726464]]
