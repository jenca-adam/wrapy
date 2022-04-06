import rfc7578

class File(rfc7578.File):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def __repr__(self):
        return f'<File name="{self.name}" mode="rb" content_type="{self.content_type}">'
    @classmethod
    def open(self,file):
        reader=open(file,'rb')
        return File(reader.read(),file)
