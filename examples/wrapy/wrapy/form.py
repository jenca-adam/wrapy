import ujson
import urllib.parse
import rfc7578
from .file import File
from .maketuple import make_tuple 
class ContentTypeError(Exception):pass
urlencode=urllib.parse.urlencode
def force_list(ob):
    if isinstance(ob,list):
        return ob
    return [ob]
def multipart(data):
    data={k:force_list(v) for k,v in data.items()}
    return rfc7578.make(data)
methods={'application/x-www-form-urlencoded':urlencode,'application/json':ujson.dumps,'multipart/form-data':multipart,'text/plain':bytes,'application/octet-stream':bytes}
def encode(data,ctype='application/x-www-form-urlencoded'):
    if not data:
        return {},b''
    if ctype not in methods:
        raise ContentTypeError(
                "invalid content type: valid form content types are " + ','.join(methods.keys())
                )
    m=methods[ctype]
    a=make_tuple(m(data),2,{})
    return a


