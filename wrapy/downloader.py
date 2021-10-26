import warnings
import urllib.parse

from .version import __version__
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
class Downloader:
    def __init__(self):
        if _client.__name__=='requests':
            self.session=_client.Session()
        if _client.__name__=='httplib2':
            self.h=_client.Http('.cache/httplib2')
    def download(self,url,num_retries=0,user_agent='python-wrapy/'+__version__):
        status_code,host=200,urllib.parse.urlsplit(url).netloc
        if _client.__name__=='httplib2':
            r,c=self.h.request(url,headers={'User-Agent':user_agent})
            if r.status>399:
                status_code=r.status
            else:
                return c
        elif _client.__name__=='requests':
            x= _client.get(url,headers={'User-Agent':user_agent})
            if x.ok:
                return x.text
            status_code=x.status_code
        elif _client.__name__=='urllib.request':
            rq=self.session.Request(url)
            rq.add_header('User-Agent',user_agent)
            try:
                return urlopen(req).read()
            except Exception as e:
                d=str(e)
                status_code=int(d[11:15])
        if status_code>=500 and num_retries:
            return self.download(url,num_retries-1,user_agent)
        message=f'Could not complete request. {status_code} was raised by {host} (requesting {url!r})'
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




