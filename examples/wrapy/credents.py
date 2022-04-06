import base64

def credentencode(username,password):
    to_encode='{}:{}'.format(username,password).encode()
    return base64.b64encode(to_encode).decode()
