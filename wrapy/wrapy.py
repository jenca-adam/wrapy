from .endpoint import *

from .module import *
from .spec import *
from .version import __version__
from .realdict import getreal
from .cacher import *
from .debug import debuglevel,debugprint as print
from .mime import independent_header,MimeTypes
from .fulldict import fullDict
from . import unique

import ujson
class ArgumentRequiredError(Exception):pass

def WraPy(root_url,num_retries=0,name='WraPy',user_agent='python-wrapy/'+__version__,main_args=[],arg_count=0,api_type='normal',args_required=False,child=None,autochild=True,root_url_fstring="{}",argmap={},headers={},kwarg_default={},arg_default=[],cache_timeout=None,enable_caching=False,**predefined_args):
    
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
        _headers=headers
        _kwarg_default=kwarg_default
        _arg_default=arg_default
        _cache_timeout=cache_timeout
        _encach=enable_caching
        if (len(_ll)>1 or '=' in _ll) and isinstance(_ll[0],str) and name=='WraPy' and _ll[0].split()[0]==_ll[0] and '(' not in _ll[0] and '[' not in _ll[0]:
            
            __qualname__=_ll[0]

        else:
            
            __qualname__=name
        _name=__qualname__
        
        def __init__(self,*args,**kwargs):
            cache_timeout=self._cache_timeout
            print('Parsing arguments')
            args=list(args)
            args,kwargs=self.__default(kwargs,args)
            kwargs.update(self.__makekwargs(self._predefined_args))
            args,k=self.__makeargs(args)
            kwargs.update(k)

            if self._encach:
                print('Caching is Enabled')
                if self._cache_timeout is None:
                    print('Setting cache_timeout to 10 minutes')
                    cache_timeout=600
                print('Creating Cacher')
                
                cacher=Cacher(cache_timeout)
                print('Loading data from cache...')
                try:
                    dc=cacher.load(args,kwargs,self.__class__.__qualname__,root_url)
                    mimetype=dc['mimetype']
                    del dc['mimetype']
                    mimetype=unique.Unique(None,mimetype)
                    self._original=ujson.loads(ujson.dumps(dc))
                    object=makeclass(dc)
                    print("Done.")

                except CachingError:
                    print('Cache expired! Retrieving again ... ')
                    print('Getting Original from server')
                    mimetype,self._original=self._endpoint(self._root_url,self._user_agent,self._root_url_fstring,self._headers).connect(num_retries,*args,**kwargs)
                    print("Calling makeclass")
                    if mimetype!=MimeTypes.IMAGE:
                        object=makeclass(ujson.loads(ujson.dumps(self._original)))
                    else:
                        object=self._original

                    print('Getting real __dict__')
                    dc=getreal(object)
            else:
                print('Getting Original from server')
                self.mimetype,self._original=self._endpoint(self._root_url,self._user_agent,self._root_url_fstring,self._headers).connect(num_retries,*args,**kwargs)
                print("Calling makeclass")
                if self.mimetype!=MimeTypes.IMAGE:
                    object=makeclass(ujson.loads(ujson.dumps(self._original)))
                else:
                    object=self._original
                print('Getting real __dict__')
                dc=getreal(object)
            if hasattr(self,'mimetype'):
                mimetype=self.mimetype
            self.mimetype=mimetype
            self.__dict__['mimetype']=mimetype
            print('Autochilding')
            if child in dc:
                
                dc=dc[child]
            
            elif len(dc)==1 and hasattr(list(dc.values())[0],'_json') and autochild:
                
                dc=list(dc.values())[0]
            print('Updating self.__dict__')
            self.__dict__.update(dc.__dict__ if hasattr(dc,'__dict__') else dc)
            #self._original=fullDict(self._original)
            if self._encach:
                print('Dumping...')
                cacher.dump(self,args,kwargs)
                print('Loaded successfully')
        def __makeargs(self,args):
            
            if args_required and len(args)!=len(self._main_args)+self._arg_count:
                
                s=''if len(self._main_args)==1 else 's'
                
                raise ArgumentRequiredError(f"'__init__' requires exactly {len(self._main_args)+self._arg_count} argument{s}, {len(args)} given")
            
            x={}
            a=[]
            
            if self._endpoint==URLEndpoint or self._endpoint==CombinedEndpoint:
                print('URL endpoint')
                if self._endpoint==URLEndpoint or not self._main_args:
                    print('Exactly')
                    a=args
                else:
                    print('Combined')
                    for i in range(self._arg_count):
                        print(f'Popping {i}') 
                        a.append(args.pop(0))
            
            if self._endpoint == ParamEndpoint or self._endpoint==CombinedEndpoint:
                print('Param endpoint')
                
                index=0
                for i in self._main_args:
                        print(f'Iterating main_arg {i}')
                        
                        try:
                            
                            x[i]=args[index]
                        
                        except IndexError:
                            print('Enough')
                            
                            break
                        
                        index+=1
            
            return [str(i) for i in a],x
        def __makekwargs(self,args):
            print('Making kwargs')
            args_iter=args.copy()
            
            for i in args_iter:
                
                if i in self._argmap:
                    print(f'Mapping {i}->{self._argmap[i]}')
                    args[self._argmap[i]]=args[i]
                    del args[i]
                else:
                    print('Not in argmap')
            return args
        def __default(self,ka,a):
            print('Making defaults')
            args=self._kwarg_default.copy()
            print('Default kw')
            args.update(ka)

            nags=self._arg_default.copy()
            print('Default args')
            for ind,i in enumerate(a):
                
                try:
                    print(f'Rewriting {nags[ind]}->{i}') 
                    nags[ind]=i
                except IndexError:
                    print(f'{i} has no default value')
                    nags.append(i)
            return nags,args

    return Result

def WraPyObject(root_url,name='Result',num_retries=0,user_agent='python-wrapy/'+__version__,**kwargs):
    
    return WraPy(root_url,user_agent=user_agent,num_retries=num_retries)(**kwargs)

