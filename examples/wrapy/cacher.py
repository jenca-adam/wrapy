from .setup import cachedir_setup
from .debug import debugprint
import time
import dill 
import hashlib
import os
import pathlib
import datetime
import timeago

cachedir_setup()
cwd=pathlib.Path(os.getcwd())
def join(*dirs):
    return os.path.join(cwd,'.cache/wrapy',*dirs)
def exists(subdir):
    pth=cwd/subdir
    return os.path.exists(pth)
class CachingError(Exception):pass
class CacheExpiredError(CachingError):pass 
class HashNotFoundError(CachingError):pass
class Cacher:
    def __init__(self,cache_timeout):
        self.cache_timeout=cache_timeout
    def makehash(self,object,args,kwargs):
        dill_encrypted_object=dill.dumps((args,kwargs,object._root_url,object.__class__.__qualname__))
        return hashlib.sha224(dill_encrypted_object).hexdigest()
    def convert(self,o,a,k,h):
        tim=time.time()
        debugprint('Preparing to dump...')
        return {
                'created':tim,
                'expires':tim+self.cache_timeout,
                'timeout':self.cache_timeout,
                'args':a,
                'kwargs':k,
                'object':o._original,
                'mimetype':o.mimetype.name,
                'fn':h,
                'root_url':o._root_url,
               }
    def dump(self,object,args,kwargs):
        debugprint('Retrieving Hash')
        secret_hash=self.makehash(object,args,kwargs)
        debugprint(f'Hash is {secret_hash!r}') 

        fn = join(secret_hash)
        if exists(fn):
            debugprint(f'{fn} exists, checking expirancy')
            z=open(fn,'rb')
            debugprint(f'Reading data')
            obj=dill.loads(z.read())
            debugprint(f'Timeout is {obj["timeout"]}')
            if obj['expires']>time.time():
                debugprint(f'Object did not yet expire. Checking eq')
                if obj['object']==object._original and obj['args']==args and obj['kwargs']==kwargs:
                    debugprint('Equal. Done')
                    return
        to_dump=self.convert(object,args,kwargs,secret_hash)
        debugprint('Dumping...')
        dumped=dill.dumps(to_dump)
        debugprint('Writing..')
        open(fn,'wb').write(dumped)
        debugprint('Dumping finished.')
    def load(self,args,kwargs,name,root_url):
        debugprint('Retrieving Hash')
        dill_encrypted_object=dill.dumps((args,kwargs,root_url,name))
        secret_hash=hashlib.sha224(dill_encrypted_object).hexdigest()
        debugprint(f'Hash is {secret_hash!r}') 
        fn = join(secret_hash)
        if not exists(fn):
            raise HashNotFoundError(f'hash not found: {secret_hash!r}. probably this object was never saved')
        fp = open(fn,'rb')
        debugprint(f'dill loading {fn}')
        obj=dill.load(fp)
        debugprint('Getting expirancy data')
        debugprint(f'Timeout is {obj["timeout"]}')
        tm=time.time()
        dtm=datetime.datetime.fromtimestamp(tm)
        if obj['expires']<=tm:
            debugprint('Expired!')
            tdl=dtm-datetime.datetime.fromtimestamp(obj['expires'])
            raise CacheExpiredError(f'cache expired {timeago.format(tdl)}')
        obj['object']['mimetype']=obj['mimetype']
        return obj['object']


