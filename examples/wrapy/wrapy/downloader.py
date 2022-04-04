import warnings
import urllib.parse
from .mime import *
from .debug import debuglevel,debugprint as print
from .version import __version__
from .form import encode
from .urllibpost  import makePost
from .credents import credentencode
warnings.filterwarnings('ignore',category=ResourceWarning)
class UsingDefaultClientWarning(UserWarning):pass
class HTTPError(Exception):pass
try:
    import httplib2
    _client=httplib2
except:
    try:
        import requests
        _client=requests
    except:
        warnings.warn(UsingDefaultClientWarning('Neither httplib2 nor requests are installed. Using default web client (urllib.request)'))
        import urllib.request
        _client=urllib.request
import http.client
http.client.HTTPConnection.debuglevel=debuglevel
if _client.__name__=='httplib2':
    _client.debuglevel=debuglevel

class Downloader:
    def __init__(self):
        if _client.__name__=='requests':
            self.session=_client.Session()
        if _client.__name__=='httplib2':
            self.h=_client.Http('.cache/httplib2')
    def download(self,
                url,
                credentials=(),
                method='GET',
                body=b'',
                num_retries=0,
                user_agent='python-wrapy/'+__version__,
                headers={},
                content_type='application/x-www-form-urlencoded'
                ):
        print(f'Requesting {url}')
        headers={'Content-Type':content_type}
        if credentials:
            authdr={'Authorization':'Basic '+credentencode(*credentials)}
            headers.update(authdr)
        status_code,host=200,urllib.parse.urlsplit(url).netloc
        
        headers=headers
        headers.update({'User-Agent':user_agent})
        if method!='GET':
            addhdr,body=encode(body,content_type)
            headers.update(addhdr)
        print(f'Client is {_client.__name__}')
        if _client.__name__=='httplib2':
            
            r,c=self.h.request(url,method=method,headers=headers,body=body)
            if r.status>399:
                status_code=r.status
                reason=r.reason
            else:
                return detect(r),c
        elif _client.__name__=='requests':
            x= _client.request(method,url,headers=headers,data=body)
            if x.ok:
                return detect(x),x.text
            status_code=x.status_code
            reason=x.reason
        elif _client.__name__=='urllib.request':
            rq=makePost(_client.Request(url),body,ctype)
            

            try:
                n=urlopen(rq)

                return detect(n),n.read()
            except Exception as e:
                d=str(e)
                status_code=int(d[11:14])
                reason=d[16:]
        if status_code>=500 and num_retries:
            print(f'Could not download, retrying with num_retries {num_retries-1} {"(!!!!)" if num_retries == 1 else ""}')
            return self.download(url,num_retries-1,user_agent)
        message=f'Could not complete request. {status_code} {reason if reason else "" } was raised by {host} (requesting {url!r})'
        raise HTTPError(message)
    def __enter__(self):
        return self
    def __exit__(self,*args):
        if _client.__name__=='requests':
            self.session.close()
        if _client.__name__=='httplib2':
            self.h.close()
downloader=Downloader()
download=downloader.download




