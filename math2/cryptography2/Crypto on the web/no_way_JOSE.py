import base64
import json
import jwt # note this is the PyJWT module, not python-jwt


SECRET_KEY = ""
FLAG = ""



def authorise(token):
    token_b64 = token.replace('-', '+').replace('_', '/') # JWTs use base64url encoding
    try:
        header = json.loads(base64.b64decode(token_b64.split('.')[0] + "==="))
    except Exception as e:
        return {"error": str(e)}

    if "alg" in header:
        algorithm = header["alg"]
    else:
        return {"error": "There is no algorithm key in the header"}

    if algorithm == "HS256":
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            return {"error": str(e)}
    elif algorithm == "none":
        try:
            decoded = jwt.decode(token, algorithms=["none"], options={"verify_signature": False})
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Cannot decode token"}

    if "admin" in decoded and decoded["admin"]:
        return {"response": f"Welcome admin, here is your flag: {FLAG}"}
    elif "username" in decoded:
        return {"response": f"Welcome {decoded['username']}"}
    else:
        return {"error": "There is something wrong with your session, goodbye"}



def create_session(username):
    encoded = jwt.encode({'username': username, 'admin': True}, SECRET_KEY, algorithm='none')
    return {"session": encoded}


#we use create_session(username) to create a jwt that will be sent to the server
#if we set algorithm=none, the server will not verify the signature with the secret key
#if we set admin=true, the flag will be revealed
username="minh"
x=create_session(username)
print(x)
x=x['session']
#submit the received token to the website
