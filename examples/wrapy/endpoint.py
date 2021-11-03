from .downloader import *
from .slasher import slash,argjoin,reslash
from .classgen import makeclass
from .version import __version__
from .mime import *

from PIL import Image
import ujson
import xmltodict
import io
class EndpointError(Exception):pass
def getEndpoint(endp_type):
    if endp_type.lower() in['normal','classic','parameters','param']:
        return ParamEndpoint
    if endp_type.lower() == 'url':
        return URLEndpoint
    if endp_type.lower() == 'combined':
        return CombinedEndpoint
class Endpoint:
    def __init__(self,root_url,user_agent='python-wrapy/'+__version__,root_fstring='{}',headers={}):
        self.root_url=slash(root_url)
        self.user_agent=user_agent
        self.root_fstring=root_fstring
        self.headers=headers
    def makeurl(self,a,k):#this must be replaced
        raise NotImplementedError
    def connect(self,num_retries=0,*args,**kwargs):
        url=reslash(self.root_url)
        if args or kwargs:  
            url=self.makeurl(args,kwargs)
        mt,r=download(url,num_retries,self.user_agent,headers=self.headers)
        if mt == MimeTypes.JSON:
            obj=ujson.loads(r)
        elif mt == MimeTypes.XML:
            obj=xmltodict.parse(r)
        elif mt == MimeTypes.IMAGE:
            return mt,Image.open(io.BytesIO(r))
        elif mt == MimeTypes.UNKNOWN:
            raise EndpointError('could not handle MIME type: WraPy supports */json, XML and image/*')
        return mt,obj
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

