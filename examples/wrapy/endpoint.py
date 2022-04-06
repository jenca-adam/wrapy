from .downloader import *
from .slasher import slash,argjoin,reslash
from .classgen import makeclass
from .version import __version__
from .mime import *
from .debug import debugprint as print
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
    if endp_type.lower() in ['post-normal','post-classic', 'post-parameters', 'post-param']:
        return PostParamEndpoint
    if endp_type.lower() == 'post':
        return PostEndpoint
    if endp_type.lower() == 'post-url':
        return PostURLEndpoint
    if endp_type.lower() == 'post-combined':
        return PostCombinedEndpoint
class Endpoint:
    def __init__(self,root_url,user_agent='python-wrapy/'+__version__,root_fstring='{}',headers={},endslash=True):
        self.root_url=slash(root_url)
        self.user_agent=user_agent
        self.root_fstring=root_fstring
        self.headers=headers
        self.slash=endslash
        print(self.slash)
    def makeurl(self,a,k):#this must be replaced
        return self.root_url
    def connect(self,num_retries=0,credentials=(),*args,**kwargs):
        url=self.reslash(self.root_url)
        if args or kwargs:  
            url=self.makeurl(args,kwargs)
        mt,r=download(url,num_retries=num_retries,user_agent=self.user_agent,credentials=credentials,headers=self.headers)
        if mt == MimeTypes.JSON:
            obj=ujson.loads(r)
        elif mt == MimeTypes.XML:
            obj=xmltodict.parse(r)
        elif mt == MimeTypes.IMAGE:
            return mt,Image.open(io.BytesIO(r))
        elif mt == MimeTypes.UNKNOWN:
            raise EndpointError('could not handle MIME type: WraPy supports */json, XML and image/*')
        return mt,obj
    def reslash(self,string):
        if self.slash:
            return reslash(string)
        return string
    
class ParamEndpoint(Endpoint):
    def makeurl(self,args,kwargs):
        return ''.join([self.root_fstring.format(self.root_url),'?',argjoin(kwargs)])

class URLEndpoint(Endpoint):
    def makeurl(self,args,kwargs):
        return self.root_fstring.format(self.reslash(self.root_url)+'/'.join(args))
class CombinedEndpoint(ParamEndpoint,URLEndpoint):
    def makeurl(self,args,kwargs):
        url=self.root_fstring.format(self.reslash(self.root_url)+('/'.join(args)))
        return ''.join([url,'?',argjoin(kwargs)])
class PostEndpoint(Endpoint):
    def __init__(self,*args,**kwargs):
        content_type=kwargs.get("content_type","application/x-www-form-urlencoded")
        if "content_type" in kwargs:
            del kwargs["content_type"]
        self.content_type=content_type
        print(args,kwargs)
        super().__init__(*args,**kwargs)
    def connect(self,num_retries=0,credentials=(),data=b'',**kwargs):
        print(data)
        url=self.makeurl(None,None)
        content_type=self.content_type 
        mt,r=download(url,method="POST",credentials=credentials,content_type=content_type,body=data,num_retries=num_retries)
        if mt == MimeTypes.JSON:
            obj=ujson.loads(r)
        elif mt == MimeTypes.XML:
            obj=xmltodict.parse(r)
        elif mt == MimeTypes.IMAGE:
            return mt,Image.open(io.BytesIO(r))
        elif mt == MimeTypes.UNKNOWN:
            raise EndpointError('could not handle MIME type: WraPy supports */json, XML and image/*')
        return mt,obj
        
        

    
