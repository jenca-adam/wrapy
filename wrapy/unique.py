from .module import searchlines
import uuid
class Unique:
    def __init__(self,id=None,name=None):
        if not id:
            self.id=uuid.uuid1().bytes
        else:
            self.id=id
        if name is None:
            self.name=searchlines('Unique',1,'UNIQUE')
        else:
            self.name=name
    def __eq__(self,other):
        return other.id==self.id or other.name==self.name
    def __repr__(self):
        return self.name
