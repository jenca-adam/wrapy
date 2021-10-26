from .wrapy import WraPy 
from .module import *
class WraPyGroup:
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        
    def WraPy(self,*args,**kwargs):
        args,kwargs=self.merge(args,kwargs)
        _ll=last_line().split('=')
        if 'name' not in kwargs and len(args)<3:

            
            if (len(_ll)>1 or '=' in _ll) and isinstance(_ll[0],str) and  _ll[0].split()[0]==_ll[0] and '(' not in _ll[0] and '[' not in _ll[0]:
                 name=_ll[0]
            else:
                name='WraPy'
        else:
            if 'name' in kwargs:
                name=kwargs['name']
                del kwargs['name']
            else:
                name=args[2]
                del args[2]

         
        return WraPy(*args,name=name,**kwargs)
    
    def merge(self,args,kwargs):
        args=list(args) 
        args.extend(self.args)

        kwargs.update(self.kwargs)
        
        return args,kwargs

