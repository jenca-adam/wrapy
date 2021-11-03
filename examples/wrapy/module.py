import inspect
import re
def module(raw=False,all=False):
    
    cf=inspect.currentframe()
    frames=[]
    while cf.f_back and cf.f_back.f_globals['__name__']not in ['__main__','importlib._bootstrap']:
        cf=cf.f_back
        frames.append(cf)
    if raw:
        if all:
            return frames
        return cf
    if all:
        return [c.f_globals['__name__'] for c in frames]

    return cf.f_globals['__name__']
def getline(cf):
    try:
        with open(cf.f_code.co_filename,'r')as f:
            return f.read().splitlines()[cf.f_lineno-1]
    except:
        return ''

def last_line():
    cf=module(True)
    return getline(cf)
def lines():
    frames=module(True,True)
    return [getline(line) for line in frames]
def frames_locals():
    cf=inspect.currentframe()
    frames=[]
    while cf.f_back:
        frames.insert(0,cf.f_locals)
        cf=cf.f_back
    return frames
def searchlines(query,side=1,caseNone=''):
    for i in lines():
        try:
            if re.search(i.split('=')[1],query):
                return i.split('=')[0].strip()
        except IndexError:pass
    return caseNone
