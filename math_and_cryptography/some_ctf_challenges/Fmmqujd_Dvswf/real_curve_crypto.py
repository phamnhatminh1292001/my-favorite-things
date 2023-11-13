import random
from sage.modules.free_module_integer import IntegerLattice
R = RealField(700)
x0 = 1.15939524880832589559531697886995971202850341796875
x1 = 1052.1869486109503324827555468817188804055933729601321435932864694301534931492427433020783168479195188024409373571681097603398390379320742186401833284576176214641603772370675124838606986281131453644941
x0 = R(x0)
x1 = R(x1)


def Babai_closest_vector(M, G, target):
    small = target
    for _ in range(1):
        for i in reversed(range(M.nrows())):
            c = ((small * G[i]) / (G[i] * G[i])).round()
            small -= M[i] * c
    return target - small


def elliptic_log(x0, y0):
    e1 = R(1)
    e2 = R(0)
    e3 = R(-1)
    a0 = R(sqrt(e1-e3))
    b0 = R(sqrt(e1-e2))
    r = R(sqrt((x0-e3)/(x0-e2)))
    t = R(-y0/(2*r*(x0-e2)))
    for i in range(0, 1000):
        x = R((a0+b0)/2)
        y = R(sqrt(a0*b0))
        r = R(sqrt(x*(r + 1)/(b0*r + a0)))
        t = R(t*r)
        a0 = x
        b0 = y
    z = (1/a0)*arctan(a0/t)
    return a0, z


R = RealField(700)
y0 = R(sqrt(x0 ^ 3-x0))
y1 = R(sqrt(x1 ^ 3-x1))
y0 = 2*y0
y1 = 2*y1

a0, z0 = elliptic_log(x0, y0)
a0, z1 = elliptic_log(x1, y1)
# the basis of the lattice
w = R(R(pi)/a0)
# the elliptic logarithm of the curve
z0 = z0+w
z1 = z1+w
print(z0)
print(z1)

# a*z0=z1+b*w0
# use cvp
for i in range(0, 900):
    B = random.randint(1, 2 ^ 273)
    div1 = int(abs(z0/z1*B))
    div2 = int(abs(w/z1*B))
    # build lattice
    A = matrix([[div1, 1, 0], [div2, 0, 1]])
    lattice = IntegerLattice(A, lll_reduce=True)
    v = vector([B, 0, 0])
    gram = lattice.reduced_basis.gram_schmidt()[0]
    res = Babai_closest_vector(lattice.reduced_basis, gram, v)
    # sol for a,b
    u = res-v
    a = u[1]
    b = u[2]
    if a > 0 and a < 2 ^ 128 and abs(a*z0+b*w-z1) < 1:
        print(a)
        print(a*z0+b*w-z1)
        print(a.bit_length())
