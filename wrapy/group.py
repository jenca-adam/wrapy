from .wrapy import WraPy as wrp
from .module import *
class WraPyGroup:
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        
    def WraPy(self,*args,**kwargs):
        if 'name' not in kwargs and len(self.args)<3:

            _ll=last_line().split('=')
            
            if (len(_ll)>1 or '=' in _ll) and isinstance(_ll[0],str) and  _ll[0].split()[0]==_ll[0] and '(' not in _ll[0] and '[' not in _ll[0]:
                    __qualname__=_ll[0]
                else:
                    __qualname__='WraPy'

 
        args,kwargs=self.merge(args,kwargs)
        return WraPy(*args,**kwargs)
    
    def merge(self,args,kwargs)
        
        args.extend(self.args)

        kwargs.update(self.kwargs)
        
        return args,kwargs

