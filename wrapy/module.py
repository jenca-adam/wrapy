import inspect
def module(raw=False):
    cf=inspect.currentframe()
    while cf.f_back and cf.f_back.f_globals['__name__']not in ['__main__','importlib._bootstrap']:
        cf=cf.f_back
    if raw:
        return cf
    return cf.f_globals['__name__']
def last_line():
    cf=module(True)
    try:
        with open(cf.f_code.co_filename,'r')as f:
            return f.read().splitlines()[cf.f_lineno-1]
    except:
        raise
        return ''
def frames_locals():
    cf=inspect.currentframe()
    frames=[]
    while cf.f_back:
        frames.insert(0,cf.f_locals)
        cf=cf.f_back
    return frames
