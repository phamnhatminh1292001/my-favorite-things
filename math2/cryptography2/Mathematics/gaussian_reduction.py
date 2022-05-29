from math import floor
from copy import deepcopy


def product(v1,v2):
    sum=0
    for i in range(0,len(v1)):
        sum+=v1[i]*v2[i]
    return sum


def gaussian_reduce(v1,v2):
    while True:
        m=product(v2,v2)-product(v1,v1)
        if m<0:
            temp=(v1)
            v1=(v2)
            v2=(temp)
        q=product(v1,v2)/product(v1,v1)
        if floor(q)==0:
            return (v1,v2)
        v2=[v2[i]-floor(q)*v1[i] for i in range(0,len(v1))]
        
    

v = [846835985, 9834798552]
u = [87502093, 123094980]




