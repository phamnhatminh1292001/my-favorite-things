# exacly what we used in backpack cryptography
#v1=[1 0 0...0 2^256*sqrt(p1)]
#v2=[0 1 0...0 2^256*sqrt(p2)]
#...
#vn=[0 0 0...1 2^256*sqrt(pn)]
#vn+1=[0 0 0... 0          ct]
#the problem is that we need an integer matrix for LLL
#thus we need to use integer value that are close to 2^256*sqrt(pi)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ROUND=[round(sqrt(i)*16**64) for i in PRIMES]
l=len(PRIMES)
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433
A=Matrix(ZZ,l+1,l+1)
for i in range(0,l):
    A[i,i]=1
for i in range(0,l):
    A[i,l]=ROUND[i]
A[l,l]=ct
print(A)
B=A.LLL()
print(B)
#turn out we got the FIRST vector
s=""
v=B[0]
for i in v[:-1]:
    s+=chr(-int(i))
print(s)
