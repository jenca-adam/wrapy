debuglevel=1
def debugprint(*args,**kwargs):
    global debuglevel
    if not debuglevel:
        return
    print(*args,**kwargs)
