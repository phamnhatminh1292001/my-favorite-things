from Crypto.Cipher import AES

import hashlib
import sys
import binascii
cipher_text_hex="c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"


#solution: BRUTE FORCE. JUST CONSIDER ALL WORDS IN THE LIST
#BECAUSE THE WORDS ARE CHOSEN RANDOMLY AND WE DON"T KNOW ANYTHING
#ELSE

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted}


with open('word.txt') as f:
    words = [w.strip() for w in f.readlines()]
for i in words:
    x=hashlib.md5(i.encode()).hexdigest()
    s=decrypt(cipher_text_hex,x)['plaintext']
    if b'crypto' in s:
        print(s)
