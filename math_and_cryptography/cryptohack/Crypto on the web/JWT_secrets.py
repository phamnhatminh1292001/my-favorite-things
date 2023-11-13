import jwt # note this is the PyJWT module, not python-jwt


SECRET_KEY = "secret" # TODO: PyJWT readme key, change later
FLAG = ""



def authorise(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        return {"error": str(e)}

    if "admin" in decoded and decoded["admin"]:
        return {"response": f"Welcome admin, here is your flag: {FLAG}"}
    elif "username" in decoded:
        return {"response": f"Welcome {decoded['username']}"}
    else:
        return {"error": "There is something wrong with your session, goodbye"}



def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, SECRET_KEY, algorithm='HS256')
    return {"session": encoded}


#the secret key is "secret", you can see it immediately by opening PyJwt page
# https://pyjwt.readthedocs.io/en/stable/ or https://gemfury.com/squarecapadmin/python:PyJWT/-/content/README.md
a=create_session('minh')
print(a)