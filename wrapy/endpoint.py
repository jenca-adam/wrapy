from .downloader import *
from .slasher import slash,argjoin,reslash
from .classgen import makeclass
from .version import __version__
import ujson
import xmltodict
class EndpointError(Exception):pass
def getEndpoint(endp_type):
    if endp_type.lower() in['normal','classic','parameters','param']:
        return ParamEndpoint
    if endp_type.lower() == 'url':
        return URLEndpoint
    if endp_type.lower() == 'combined':
        return CombinedEndpoint
class Endpoint:
    def __init__(self,root_url,user_agent='python-wrapy/'+__version__,root_fstring='{}'):
        self.root_url=slash(root_url)
        self.user_agent=user_agent
        self.root_fstring=root_fstring
    def makeurl(self,a,k):#this must be replaced
        raise NotImplementedError
    def connect(self,num_retries=0,*args,**kwargs):
        url=reslash(self.root_url)
        if args or kwargs:  
            url=self.makeurl(args,kwargs)
        
        r=download(url,num_retries,self.user_agent)
        try:
            obj=ujson.loads(r)
        except ValueError:
            try:
                obj=xmltodict.parse(r)
            except:
                raise EndpointError(f'could not determine format: not well-formed(downloading {url!r})')

        return makeclass(obj)
class ParamEndpoint(Endpoint):
    def makeurl(self,args,kwargs):
        return ''.join([self.root_fstring.format(self.root_url),'?',argjoin(kwargs)])

class URLEndpoint(Endpoint):
    def makeurl(self,args,kwargs):
        return self.root_fstring.format(reslash(self.root_url)+'/'.join(args))
class CombinedEndpoint(ParamEndpoint,URLEndpoint):
    def makeurl(self,args,kwargs):
        url=self.root_fstring.format(reslash(self.root_url)+('/'.join(args)))
        return ''.join([url,'?',argjoin(kwargs)])

