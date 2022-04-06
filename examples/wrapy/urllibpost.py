from .form import encode
def makePost(request,body,ctype):
    request.method='POST'
    request.data=encode(body,ctype)
    return request
