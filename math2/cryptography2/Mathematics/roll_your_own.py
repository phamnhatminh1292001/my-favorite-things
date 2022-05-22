#!/usr/local/bin/python3

from Crypto.Util.number import getPrime
import random
import json

flag = b'crypto{???????????????????????????????????}'

def input_json(prompt: str):
    data = input(prompt)
    try:
        return json.loads(data)
    except:
        print({"error": "Input must be sent as a JSON object"})
        exit()


def check_params(data, q):
    g = int(data['g'], 16)
    n = int(data['n'], 16)
    if g < 2:
        return False
    elif n < 2:
        return False
    elif pow(g,q,n) != 1:
        return False
    return True


def main():
    q = getPrime(512)
    x = random.randint(2,q)
    print(f"Prime generated: {hex(q)}")

    data = input_json('Send integers (g,n) such that pow(g,q,n) = 1: ')
    check = check_params(data, q)

    if check:
        g = int(data['g'], 16)
        n = int(data['n'], 16)
        h = pow(g,x,n)
        print(f'Generated my public key: {hex(h)}')
    else:
        print({"error": "Please ensure pow(g,q,n) = 1"})
        exit()

    data = input_json('What is my private key: ')

    if int(data['x'], 16) == x:
        print({"flag": flag})
    else:
        print({"error": "Something has gone wrong with your calculation!"})
        exit()

if __name__ == '__main__':
    main()
