def make_tuple(d,l,ev=None):
    if isinstance(d,tuple):
        if len(d)>=l:
            return d[len(d)-l:]
        else:
            return (ev,)*l-len(d)+d
    else:
        return (ev,)*(l-1)+(d,)
