#!/usr/bin/env python3
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Hash import SHA256
import base64
from gmpy2 import mpz,gcd
import requests
import jwt
#we would like to find N and e, they are the public keys
#e must be 65537, thus N is enough
#we have sign[0]^65537=m[0] (mod N) and sign[1]^65537=m[1] (mod N) and sign[2]^65537=m[2] (mod N)

#copy the encode and decode from the utils module of pyjwt
def base64url_decode(input):
    input = input.encode('ascii')
    rem = len(input) % 4
    if rem > 0:
        input += b'=' * (4 - rem)
    t=base64.urlsafe_b64decode(input)
    return t

def base64url_encode(input):
    return base64.urlsafe_b64encode(input).replace(b'=', b'')

jjwt=[]
#some keys
jjwt.append("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6Im1pbmgiLCJhZG1pbiI6ZmFsc2V9.xm3WjZjILOQ6LJOJ9Rr_scHdb4SOvmmMc_P7tG2CZhyuB0-VF1PKCHTp2H4jay6MKG1dCFyR8XGm7elIglHVz1swKSn04fumuIemkEsJPfkUmZ386Y4Q3JksN4AMpCs_VTVLbgHR5OS4UiRSY0i6cDXj0RfmEe8WeQ5o-wZ1QlHO8PphVkoxG5UVoFW4eaR4QAWr1g-vSS9ZstNZBlEG-CvcylTOn7W6g6aFtu3EJlqI0i1BFzsyCJsO-APrv8MvHoK8aUET_yuXAmxoMODexmhSHjsBYCCsKdGOUu5pOyQTKGN3EYT78Lort6_D1GhJRSJdg2KFvCFJkvqYjS5VKg")
jjwt.append("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6InRhbWEiLCJhZG1pbiI6ZmFsc2V9.AUW-9sXnY8fqaT2qQLXkj8haHTTbWPTqQD8nUoH_z1MkaohuSjE8PXvgh4Vz_nZryzkMvy5UcBZHDOdrbv96CWnD_xNVNLoIBsjTOYNBwhr6Wrck9seWCMEt8Ic3ty9PNrfF2tlz7MVOCTwyhcnPD5xshO8gfJVwSWJG96ly3oPMyZHLGsqHO2LtQvQOXyiPbFAOZ1cjXg1t_ZjsU1OzVSH8PmyagzLkrvpdTWpwaHR9Lue8a4-MFV26OGndI5i3jL_jMbWxbLZDg212j9Sf8mmCLfqETLaOEEJ2RLMaxCcD6pfR3sh1elO-j2ldjkVQpBs0w2fN_KN7YU3Mpn0h5g")
jjwt.append("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImRlYWQiLCJhZG1pbiI6ZmFsc2V9.l8WNydtpzr9-nkYyTfH--zY1C7wZXwqBmKpbg2L0ohRsb6LYdq8xBp-kkBJCmj2CYaLaW6HBoES5BY8n8NvABZ69okH9qJbF9eA5MOWXbVIxA9laLrWODdiyU7icPyrg-_yCnfK-50B52oyJ_myhzrNFAHimLPyLCNSHP2uRJ3_z4QNE92G-U78OZ9CZ5uxRQQNCZbBUMi_sLJ8D6YMEGcM07pEVBdTe22U4Ozkg_Ok__Z251mGzMC7SXrAA-ZQj8CBc4A0MQrf2HM2DRyLtbutwEK5oTpNBIX1WKTD5-lF8Zh8iJlNREDMlkGBgCY9fJQtyF0T6YxpO_328f6gk9g")
jjwt.append("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYmIiLCJhZG1pbiI6ZmFsc2V9.e-V6vhxxepTLUG3diuLPWNBqxUu-6nWTPR4Cuf2oO75UIzp0e0f2mFTZwhqQ3v-Pw_YZzj-wR8ouBJfcsfmSMDuiYumsAEAklIms60aCaHY5SAO9wg4unMv9KmOUqWL6yDaCuBN430GqwSSeG6ApbcjaUFWJ4T-z5QIBpi_lHo8MeJ3z5-LpyJiq5vc3kivwNgghKOfYVT4FbXQiwxxD-HbwndkZehm_ACONJQtk1ct2gwUZrPl6Rghin-BqI4gHpgdFHTcyK4uAcJvhZ1dkFUeyAfxYFlg84aYaxY3EVGJcU8aq5dJNWcZ491CoeiQujZ0eAybKbDWhbRr0eSmPeg")
sign=[]
sign_input=[]
h=[]
pad=[]
m=[]
for i in range(0,3):
    sign.append(base64url_decode(jjwt[i].split('.')[2]))
    sign_input.append(".".join(jjwt[i].split('.')[0:2]))
#hash the sign input, we must use the SHA256 from Crypto.Hash because pkcs1_15 uses some attributes of this
#SHA256
    h.append(SHA256.new(sign_input[i].encode()))
#pad the sign input
    pad.append(pkcs1_15._EMSA_PKCS1_V1_5_ENCODE(h[i],len(sign[i])))
    m.append(mpz(bytes_to_long(pad[i])))
    sign[i]=mpz(bytes_to_long(sign[i]))
e=65537
#we use gmpy2 because it is much faster than math.gcd
N=gcd(pow(sign[0],65537)-m[0],pow(sign[1],65537)-m[1])
N=gcd(pow(sign[2],65537)-m[2],N)
print(N)
#found the right N
N=30119723976045246500887959920897642376905514522104705876695572516818975656665827754462226597973931127004963194508794779495518118035029841228002850562126612806174354282950756669656076190799693066363785733231859172664786298352294594850108982261525326147060353679479844558827458650965802914077525964824412575118501773357860374735206849817271524812002047307305597712628593230518376740507962518305824812671107459660525177087958778694060270468673690931325503094560625544374011735643694318730778241846282742819834483180624645324880062782719575587058519516842316778261924794437716972651884728674806670910304714203419102131413


def blocks(x, n):
    return [x[i:i+n] for i in range(0, len(x), n)]


key= RSA.construct((N,e))
pubkey = key.publickey().exportKey().splitlines()
#remove the padding
pubkey[1] = pubkey[1][32:]
pubkey = b"\n".join([b"-----BEGIN RSA PUBLIC KEY-----"] + blocks(b"".join(pubkey[1:-1]), 64) + [b"-----END RSA PUBLIC KEY-----", b""])


def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, pubkey, algorithm='HS256')
    return {"session": encoded}

def authorise(token):
    url = "http://web.cryptohack.org/rsa-or-hmac-2/authorise/"
    r = requests.get(url+token+'/')
    return r.json()

encoded=create_session('minh')['session'].decode()
decoded=authorise(encoded)
print(decoded)



