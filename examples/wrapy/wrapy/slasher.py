def slash(url):
    if url.endswith('/'):
        return url[:-1]
    return url
def reslash(url):
    if url.endswith('/'):
        return url
    return url+'/'

def argjoin(args):
    para=[]
    for key in args:
        value=args[key]
        para.append(f'{key}={value}')
    return '&'.join(para)
