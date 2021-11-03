debuglevel=0
def debugprint(*args,**kwargs):
    if not debuglevel:
        return
    print(*args,**kwargs)
