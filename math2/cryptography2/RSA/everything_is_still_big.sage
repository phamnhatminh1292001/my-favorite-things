#everything thanks to this paper https://link.springer.com/content/pdf/10.1007/3-540-48910-X_1.pdf
#i understand what boneh durfee does now, had to admit they picked a very beaufitul lattice matrix
#now just have to implement the algorithm


e=0x2c998e57bc651fe4807443dbb3e794711ca22b473d7792a64b7a326538dc528a17c79c72e425bf29937e47b2d6f6330ee5c13bfd8564b50e49132d47befd0ee2e85f4bfe2c9452d62ef838d487c099b3d7c80f14e362b3d97ca4774f1e4e851d38a4a834b077ded3d40cd20ddc45d57581beaa7b4d299da9dec8a1f361c808637238fa368e07c7d08f5654c7b2f8a90d47857e9b9c0a81a46769f6307d5a4442707afb017959d9a681fa1dc8d97565e55f02df34b04a3d0a0bf98b7798d7084db4b3f6696fa139f83ada3dc70d0b4c57bf49f530dec938096071f9c4498fdef9641dfbfe516c985b27d1748cc6ce1a4beb1381fb165a3d14f61032e0f76f095d
N=0x665166804cd78e8197073f65f58bca14e019982245fcc7cad74535e948a4e0258b2e919bf3720968a00e5240c5e1d6b8831d8fec300d969fccec6cce11dde826d3fbe0837194f2dc64194c78379440671563c6c75267f0286d779e6d91d3e9037c642a860a894d8c45b7ed564d341501cedf260d3019234f2964ccc6c56b6de8a4f66667e9672a03f6c29d95100cdf5cb363d66f2131823a953621680300ab3a2eb51c12999b6d4249dde499055584925399f3a8c7a4a5a21f095878e80bbc772f785d2cbf70a87c6b854eb566e1e1beb7d4ac6eb46023b3dc7fdf34529a40f5fc5797f9c15c54ed4cb018c072168e9c30ca3602e00ea4047d2e5686c6eb37b9


A=(N+1)//2
X=int(e^0.26)
Y=int(e^0.50048)
P.<x,y> = PolynomialRing(ZZ)
f=-1+x*(A+y)
m=4

plist=[]
for i in range (0,m+1):
    for j in  range (0,i+1):
        plist.append(x^(i-j)*e^(m-j)*f^j)
for j in  range (0,m+1):
        plist.append(y*e^(m-j)*f^j)

mono=[]
for i in range (0,m+1):
    for j in  range (0,i+1):
        mono.append(x^i*y^j)
for j in  range (0,m+1):
        mono.append(x^j*y^(j+1))


value=[]
for i in range (0,m+1):
    for j in  range (0,i+1):
        value.append(X^i*Y^j)
for j in  range (0,m+1):
        value.append(X^j*Y^(j+1))


l=len(plist)
M=Matrix(ZZ,l,l)
for i in range(0,l):
    for j in range(0,l):
        M[i,j]=plist[i].monomial_coefficient(mono[j])*value[j]
        

Z=M.LLL()
#fortunately, we have found 2 polynomials with new0(k,s)=new1(k,s)=0
#thus we just need to solve an equation system
new0=P(0)
for i in range(0,l):
    new0+=Z[0][i]//value[i]*mono[i]

new1=P(0)
for i in range(0,l):
    new1+=Z[1][i]//value[i]*mono[i]

#for 2 polynomials P(x,y) and Q(x,y) resultant will give a polynomial H(x,y)=F(x,y)P(x,y)+G(x,y)Q(x,y)
#such that the degree of x in H is lowest possible, this process is like this:
#Let P(x,y)=P0(y)+x*P1(y)+x^2*P2(y)+... and Q(x,y)=Q0(y)+x*Q1(y)+x^2*Q2(y)+... now we can see both of 
#them as polynomials in x with coefficients in y. Similarly, use Euclidean algorithm to make the
#degree of x in each polynomials lower and finally finding a polynomial H(x,y)=H0(y)+x*H1(y)+x^2*H1(y)+...
#with the degree of x in H is lowest possible.
b=new1.resultant(new0)
PR.<q> = PolynomialRing(ZZ)
b=b(q,q)
s=b.roots()[0][0]

#now we just need to solve p and q

u=q^2+2*q*s+N
p=u.roots()[0][0]
q=u.roots()[1][0]
#found p and q, the rest is just decrypt
phi=(p-1)*(q-1)

d=pow(e,-1,phi)
