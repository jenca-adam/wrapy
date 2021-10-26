from .endpoint import *
from .module import *
from .spec import *
from .version import __version__


class ArgumentRequiredError(Exception):pass

def WraPy(root_url,num_retries=0,name='WraPy',user_agent='python-wrapy/'+__version__,main_args=[],arg_count=0,api_type='normal',args_required=False,child=None,autochild=True,root_url_fstring="{}",argmap={},**predefined_args):
    
    class Result:
        
        __module__=module()
        _root_url=root_url
        _user_agent=user_agent
        _num_retries=num_retries
        _ll=last_line().split('=')
        _predefined_args=predefined_args
        _main_args=main_args
        _child=child
        _api_type=api_type
        _argmap=argmap
        _endpoint=getEndpoint(api_type)
        _root_url_fstring=root_url_fstring
        _arg_count=arg_count
        
        if (len(_ll)>1 or '=' in _ll) and isinstance(_ll[0],str) and name=='WraPy' and _ll[0].split()[0]==_ll[0] and '(' not in _ll[0] and '[' not in _ll[0]:
            
            __qualname__=_ll[0]

        else:
            
            __qualname__=name
        
        def __init__(self,*args,**kwargs):
            
            args=list(args)
            kwargs.update(self.__makekwargs(self._predefined_args))
            args,k=self.__makeargs(args)
            kwargs.update(k)
            dc=self._endpoint(self._root_url,self._user_agent,self._root_url_fstring).connect(num_retries,*args,**kwargs).__dict__
            
            if child in dc:
                
                dc=dc[child]
            
            elif len(dc)==1 and hasattr(list(dc.values())[0],'_json') and autochild:
                
                dc=list(dc.values())[0]
            
            self.__dict__.update(dc.__dict__ if hasattr(dc,'__dict__') else dc)
        def __makeargs(self,args):
            
            if args_required and len(args)!=len(self._main_args)+self._arg_count:
                
                s=''if len(self._main_args)==1 else 's'
                
                raise ArgumentRequiredError(f"'__init__' requires exactly {len(self._main_args)+self._arg_count} argument{s}, {len(args)} given")
            
            x={}
            a=[]
            
            if self._endpoint==URLEndpoint or self._endpoint==CombinedEndpoint:
                
                for i in range(self._arg_count):
                    
                    a.append(args.pop(0))
            
            if self._endpoint == ParamEndpoint or self._endpoint==CombinedEndpoint:
                
                index=0
                for i in self._main_args:
                        
                        try:
                            
                            x[i]=args[index]
                        
                        except IndexError:
                            
                            break
                        
                        index+=1
            
            return [str(i) for i in a],x
        def __makekwargs(self,args):
            
            args_iter=args.copy()
            
            for i in args_iter:
                
                if i in self._argmap:
                
                    args[self._argmap[i]]=args[i]
                    del args[i]
            
            return args

    return Result

def WraPyObject(root_url,name='Result',num_retries=0,user_agent='python-wrapy/'+__version__,**kwargs):
    
    return WraPy(root_url,user_agent=user_agent,num_retries=num_retries)(**kwargs)

