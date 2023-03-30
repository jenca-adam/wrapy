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
        return FutureObject(_self.c[a],_self.cl)
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
    def __call__(_self,fn):
        return _self.function(fn)
def future(c,d):
    for i in d:
        if callable(d[i]):
            if isinstance(c.get(i,None),list):
                print(f'setting on {i}')

                for x in c[i]:
                    print(f'setting on {x}')
                    x.__dict__[i]=c[i]
                return

            c[i]=d[i]

        elif isinstance(d[i],dict) and i in c:
            if not hasattr(c.get(i,None),'__dict__'):
                continue

            if isinstance(c.get(i,None),list):
                for x in c[i]:
                    print(f'setting on {x}')
                    
                    future(x.__dict__,d[i])
                return
            print(i)
            future(c[i].__dict__,d[i])
    print(c)

