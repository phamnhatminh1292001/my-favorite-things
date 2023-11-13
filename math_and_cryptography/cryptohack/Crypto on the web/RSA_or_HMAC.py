
import requests
import jwt


def get_pubkey():
    url = "http://web.cryptohack.org/rsa-or-hmac/get_pubkey/"
    r = requests.get(url)
    return r.json()['pubkey']

PUBLIC_KEY=get_pubkey()



def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, PUBLIC_KEY, algorithm='HS256')
    return {"session": encoded}

def authorise(token):
    url = "http://web.cryptohack.org/rsa-or-hmac/authorise/"
    r = requests.get(url+token+'/')
    return r.json()

encoded=create_session('minh')['session'].decode()
decoded=authorise(encoded)
print(decoded)

    

