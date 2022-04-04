def unify(d):
    da=d.copy()
    for i in da.values():
        if isinstance(i,dict):
            d.update(unify(i))
    return d
