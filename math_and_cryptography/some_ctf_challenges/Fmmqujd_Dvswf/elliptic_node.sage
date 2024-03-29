
gx =8742397231329873984594235438374590234800923467289367269837473862487362482
gy =225987949353410341392975247044711665782695329311463646299187580326445253608
x1=2582928974243465355371953056699793745022552378548418288211138499777818633265 
y1=2421683573446497972507172385881793260176370025964652384676141384239699096612
p=4368590184733545720227961182704359358435747188309319510520316493183539079703
## y^2=x^3+ax+b (mod p)
## gy^2=gx^3+agx+b (mod p)
a=(y1**2-gy**2-x1**3+gx**3)*pow(x1-gx,-1,p)%p
b=(y1**2-x1**3-a*x1)%p

# the problem is if we use singluar curve, then there is an isomorphism from E
# to Fp or Fp^2. Suppose E: y^2=(x-a)*(x-b)^2
P.<x> = PolynomialRing(GF(p))
g=x^3+a*x+b

s=g.roots()[1][0]
g=g(x+s)

t = GF(p)(g.list()[2]).square_root()

U = (gx-s, gy)
V = (x1-s, y1)
u = (U[1]+t*U[0])/(U[1]-t*U[0]) % p
v = (V[1]+t*V[0])/(V[1]-t*V[0]) % p
v.log(u)

#reference: https://people.cs.nctu.edu.tw/~rjchen/ECC2012S/Elliptic%20Curves%20Number%20Theory%20And%20Cryptography%202n.pdf
