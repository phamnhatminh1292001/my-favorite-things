#!/usr/bin/env python3

import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes

FLAG = b"crypto{???????????????????????}"
PRIME = 77793805322526801978326005188088213205424384389488111175220421173086192558047


def _eval_at(poly, x, prime):
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def make_deterministic_shares(minimum, shares, secret, prime):
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")

    coefs = [secret]
    for i in range(1, shares + 1):
        coef = hashlib.sha256(coefs[i-1]).digest()
        coefs.append(coef)
    coefs = [int.from_bytes(p, 'big') for p in coefs]
    poly = coefs[:minimum]


    points = []
    for i in range(1, shares + 1):
        point = _eval_at(poly, coefs[i], prime)
        points.append((coefs[i], point))

    return points

share=(105622578433921694608307153620094961853014843078655463551374559727541051964080, 
25953768581962402292961757951905849014581503184926092726593265745485300657424)
a1=share[0]
a2= hashlib.sha256(long_to_bytes(a1)).digest()
a2=int.from_bytes(a2,'big')
a0=(share[1]-(a2+1)*a1**2)%PRIME
for i in range(0,128):
    decrypted=long_to_bytes(a0)
    if b'crypto' in decrypted:
        print(decrypted)
        break
    a0+=PRIME