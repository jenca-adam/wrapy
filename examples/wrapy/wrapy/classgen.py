from .module import module
from .pluralizer import plural,singular
from .debug import debugprint as print
import ujson,time
def parselist(l,name='Item'):
    print(f'Parsing list called {name}')
    ix=0
    for i in l:
        print(f'Parsing item {i}')
        if isinstance(i,dict):
            l[ix]=makeclass(i,name=singular(name))
        elif isinstance(i,list):
            l[ix]=parselist(i)
        ix+=1
    return l
def parsejson(jsonc):
    print('Parsing json')
    if isinstance(jsonc,list):
        jsonc={'items':jsonc}
    json=jsonc.copy()

    for q in jsonc:
        print(f'parsing {q!r}')
        if isinstance(json[q],dict):
            json[q]=makeclass(json[q],name=str(q).capitalize())
        elif isinstance(json[q],list):
            json[q]=parselist(json[q],name=str(q).capitalize())
    return json
def makeclass(json,name='Result'):

    print(f'Making {name}')
    if json == {}:
        return json
    class Result:
        _dict={}
        __qualname__=name
        __module__=module()
        _json=parsejson(json)
        def __init__(self):
            self._dict.update({key.replace('@','').replace('-','').replace('.','').replace('+','').replace("$",'').replace('"','').replace("'",'').replace('[','').replace(']','').replace('(','').replace(')','').replace('<','').replace('>','').replace('!','').replace('#','').replace('%','').replace('^','').replace('&','').replace('*','').replace(',','').replace(' ','').replace(';','').replace('/','').replace('+','').replace('\\',''):value for key,value in self._json.items()})
            self.__dict__=self._dict
        def __getattr__(self,attr):
            try:
                return self._dict[attr]
            except:
                raise AttributeError from None
        def __getitem__(self,i):
            return self._dict[i]
    return Result()
