def getreal(object):
    return {key:getattr(object,key) for key in dir(object)}
