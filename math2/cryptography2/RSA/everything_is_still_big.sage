
e=0x2c998e57bc651fe4807443dbb3e794711ca22b473d7792a64b7a326538dc528a17c79c72e425bf29937e47b2d6f6330ee5c13bfd8564b50e49132d47befd0ee2e85f4bfe2c9452d62ef838d487c099b3d7c80f14e362b3d97ca4774f1e4e851d38a4a834b077ded3d40cd20ddc45d57581beaa7b4d299da9dec8a1f361c808637238fa368e07c7d08f5654c7b2f8a90d47857e9b9c0a81a46769f6307d5a4442707afb017959d9a681fa1dc8d97565e55f02df34b04a3d0a0bf98b7798d7084db4b3f6696fa139f83ada3dc70d0b4c57bf49f530dec938096071f9c4498fdef9641dfbfe516c985b27d1748cc6ce1a4beb1381fb165a3d14f61032e0f76f095d
N=0x665166804cd78e8197073f65f58bca14e019982245fcc7cad74535e948a4e0258b2e919bf3720968a00e5240c5e1d6b8831d8fec300d969fccec6cce11dde826d3fbe0837194f2dc64194c78379440671563c6c75267f0286d779e6d91d3e9037c642a860a894d8c45b7ed564d341501cedf260d3019234f2964ccc6c56b6de8a4f66667e9672a03f6c29d95100cdf5cb363d66f2131823a953621680300ab3a2eb51c12999b6d4249dde499055584925399f3a8c7a4a5a21f095878e80bbc772f785d2cbf70a87c6b854eb566e1e1beb7d4ac6eb46023b3dc7fdf34529a40f5fc5797f9c15c54ed4cb018c072168e9c30ca3602e00ea4047d2e5686c6eb37b9


A=(N+1)//2
X=int(e^0.26)
Y=int(e^0.50048)
P.<x,y> = PolynomialRing(ZZ)
f=-1+x*(A+y)
plist=[P(e^3),e^3*x,e^2*f,x^2*e^3,x*e^2*f,e*f^2,x^3*e^3,x^2*f*e^2,x*f^2*e,f^3,y*e^3,y*f*e^2,y*f^2*e,y*f^3]
mono=[P(1),x,x*y,x^2,x^2*y,x^2*y^2,x^3,x^3*y,x^3*y^2,x^3*y^3,y,x*y^2,x^2*y^3,x^3*y^4]
value=[1,X,X*Y,X^2,X^2*Y,X^2*Y^2,X^3,X^3*Y,X^3*Y^2,X^3*Y^3,Y,X*Y^2,X^2*Y^3,X^3*Y^4]
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


#but the problem is that i don't know the syntax and actually i found one but it couldn't solve the equation
#but the only way to solve new(x0,y0)=0 is to find another new1 such that new1(x0,y0)=0, since there is no way
#we can solve an equation with two variables.
#i decided to look at https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage to see how he solves
# new0(x,y)=0 and he also found 2 polynomials and solve the system equation too. The following is the script to solve
#this will help us find s=(p+q)//2, from now on i will use this to find multivariate polynomial equation system
b=new1.resultant(new0)
PR.<q> = PolynomialRing(ZZ)
b=b(q,q)
s=b.roots()[0][0]

#now we just need to solve p and q

u=q^2+2*q*s+N
p=u.roots()[0][0]
q=u.roots()[1][0]
print(q)
print(p)
