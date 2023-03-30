def fullList(l):
    x=[]
    for i in l:
        x.append(fullItem(i))
    return x
def fullItem(n):
    
    if isinstance(n,dict):
        return fullDict(n)
    elif isinstance(n,list):
        return fullList(n)
    elif hasattr(n,'__dict__'):
        return n.__dict__
    else:
        return n

def fullDict(d):
    x={}
    for i in d:
        n=d[i]
        i=fullItem(i)
        x[i]=fullItem(n)
    return x
