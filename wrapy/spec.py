from .unify import *
def _find_spec_old(x):
    for i in x:
        print(x[i]) 
        if isinstance(i,str):
            if hasattr(x[i],'_user_agent'):
                return i
            if isinstance(x[i],dict):
                if _find_spec_old(x[i]):
                    return _find_spec_old(x[i])
        elif isinstance(i,dict):
            if _find_spec_old(i):
                return _find_spec_old(i)
            if _find_spec_old(x[i]):
                return _find_spec_old(x[i])
        if isinstance(i,dict):
            for c in i:
                print(c)
                if isinstance(c,str):
                    if hasattr(i[c],'_user_agent'):
                        return c
                    if isinstance(i[c],dict):
                        if _find_spec_old(i[c]):
                            return _find_spec_old(i[c])
                elif isinstance(c,dict):
                    if _find_spec_old(c):
                        return _find_spec_old(c)
                    if _find_spec_old(i[c]):
                        return _find_spec_old(i[c])
def find_spec(x):
    for y in x:
        y=unify(y)
        print(y)
        for i in y:
            if hasattr(y[i],'_user_agent'):
                return i
