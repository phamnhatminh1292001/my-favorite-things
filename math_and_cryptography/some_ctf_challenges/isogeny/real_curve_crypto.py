import hashlib
from random import *
from sage.all import *
import sys
import time

print("thinking...")
sys.stdout.flush()


# PSIDH class code is adapted from
# https://github.com/grhkm21/CTF-challenges/blob/master/Bauhinia-CTF-2023/Avengers/public/chasher.sage
proof.all(False)

x = var('x')


class PSIDH:
    def __init__(self, l):
        self.n = len(l)
        self.l = l
        self.p = 4 * product(self.l) - 1
        assert is_prime(self.p)

        self.K = GF(self.p**2, modulus=x**2 + 1, names='i')
        self.i = self.K.gen(0)
        self.sk = [randrange(-1, 2) for _ in ell]
        self.paramgen()
        self.Ex = EllipticCurve(self.K, [1, 0])

    def paramgen(self):
        E0 = EllipticCurve(self.K, [1, 0])

        # Move to random starting supersingular curve
        self.E0, _ = self.action(
            E0, E0(0), self.sk)
        self.P0 = self.E0.random_point()

    def action(self, E, PP, priv):
        assert len(priv) == self.n

        E = EllipticCurve(self.K, E.ainvs())
        PP = E(PP)
        es = priv.copy()

        while any(es):
            E.set_order((self.p + 1)**2)

            P = E.lift_x(ZZ(randrange(self.p)))
            s = [-1, 1][P[1] in GF(self.p)]
            k = prod(l for l, e in zip(self.l, es) if sign(e) == s)
            P *= (self.p + 1) // k

            for i, (l, e) in enumerate(zip(self.l, es)):
                if sign(e) != s:
                    continue

                Q = k // l * P
                if not Q:
                    continue
                Q.set_order(l)
                psi = E.isogeny(Q)

                E, P, PP = psi.codomain(), psi(P), psi(PP)
                es[i] -= s
                k //= l

        return E, PP

    def to_secret(self, E, P):
        return hashlib.sha256((str(E.j_invariant()) + str(P.xy())).encode()).hexdigest()


ell = list(prime_range(200, 450)) + [1483]
psidh = PSIDH(ell)

i = psidh.i

Ea = [33372528499672393872332590404181416281916893767235140466916831863614801026578169431437047189542815947660222,
      29251346035624752441454391002297778492944974945926857839021267687989541093702494066980866368261873469042754]
Pa = [1736180410836739977403947480765326158744959592387436445161384473728836302784684233439524520562065120321673*i + 13235718372314076047293241601229037692773561506797510084771211505954749693417156108565454989915136327960129,
      23129728691214140396800897117430098499884570579193423664903674970645166054032862211338225177761599240866114*i + 6125781729791115333939986636775593865427151381690136994934176150767696116689183269425351812534862646370235]
Ea = EllipticCurve(psidh.K, Ea)
Pa = Ea(Pa)

# For simplicity, let phi(i,b) denotes the isogeny of degree l_i and a[i]=b
# and let phihat is its dual isogeny. Now, consider a[0]=1, then the dual
# isogeny phihat(0,-1)=[-1,0,...,0]*Ea will send P0 to l_0*P0, and thus, the
# order of this new point is equal to (p+1)//l_0
# So, to check if a[0]=1, we compute Eb, Pb=action(Ea,Pa,[-1,0,...,0]) and
# check if (p+1)//l_0*Pb=INFINITY. If yes, then a[0]=1. Similarly when a[0]=-1
# If all case fails, then a[0]=0
a2 = []

for j in range(0, len(ell)):
    # a2 is our recovery key
    print(a2)
    # case 1: apply Eb, Pb = action(Ea,Pa,[-1,0,...,0])
    Eb, Pb = psidh.action(Ea, Pa, [0]*j+[1]+[0]*(len(ell)-j-1))
    Pb = Pb*((psidh.p+1)//ell[j])
    # check if Pb is equal to INFINITY, if yes, then a[0]=1
    if Pb[2] == 0:
        a2.append(-1)
        continue
    # case 2: Eb, Pb = action(Ea,Pa,[1,0,...,0])
    Eb, Pb = psidh.action(Ea, Pa, [0]*j+[-1]+[0]*(len(ell)-j-1))
    Pb = Pb*((psidh.p+1)//ell[j])
    if Pb[2] == 0:
        a2.append(1)
        continue
    # if all cases fail, then a[0]=0
    a2.append(0)

E = EllipticCurve(psidh.K, [1, 0])
P = E([0, 0])

Eab, Pab = psidh.action(E, P, a2)
sec = psidh.to_secret(Eab, Pab)
print(sec)
# dice{keep_your_p_to_yourself_7f5630dcf4}
