import functools
from .debug import debugprint as print
class FutureObject:
    def __init__(_self,c,cl):
        _self.c=c
        _self.cl=cl
        _self.__dict__={'c':c,'cl':cl}
    def __getattr__(_self,a):
        if a not in _self.c:
            _self.c.update({a:{}})
        return FutureObject(_self.c[a])
    def function(_self,fn):
        @functools.wraps(fn)
        def decorated(*args,**kwargs):
            try:
                return fn(*args,**kwargs)
            except TypeError:
                print(_self.cl._inst)
                return fn(_self.cl._inst,*args,**kwargs)
        _self.c.update({fn.__name__:decorated})
        _self.__dict__[fn.__name__]=decorated
def future(c,d):
    print('future called')
    for i in d:
        if callable(d[i]):
            print(f'{i} is a function')       
            c[i]=d[i]
        elif isinstance(d[i],dict) and i in c:
            print(f'{i} is a dict')
            future(c[i].__dict__,d[i])
