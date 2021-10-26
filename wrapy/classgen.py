from .module import module
from .pluralizer import plural,singular
def parselist(l,name='Item'):
    ix=0
    for i in l:
        if isinstance(i,dict):
            l[ix]=makeclass(i,name=singular(name))
        elif isinstance(i,list):
            l[ix]=parselist(i)
        ix+=1
    return l
def parsejson(jsonc):
    if isinstance(jsonc,list):
        jsonc={'items':jsonc}
    json=jsonc.copy()

    for q in jsonc:
        if isinstance(json[q],dict):
            json[q]=makeclass(json[q],name=str(q).capitalize())
        elif isinstance(json[q],list):
            json[q]=parselist(json[q],name=str(q).capitalize())
    return json
def makeclass(json,name='Result'):
    class Result:
        _dict={}
        __qualname__=name
        __module__=module()
        _json=parsejson(json)
        def __init__(self):
            self._dict.update({key.replace('@',''):value for key,value in self._json.items()})
            self.__dict__=self._dict
        def __getattr__(self,attr):

            return self._dict[attr]
        def __getitem__(self,i):
            return self._dict[i]
    return Result()
