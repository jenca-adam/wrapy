import wrapy

User=wrapy.WraPy('https://randomuser.me/api/')
Location=wrapy.WraPy('https://nominatim.openstreetmap.org/search/',num_retries=3,main_args=['q'],args_required=True,format='xml')
ArchivedArticle=wrapy.WraPy('https://api.nytimes.com/svc/archive/v1/',api_type='combined',root_url_fstring='{}.json',arg_count=2,argmap={'api_key':'api-key'},api_key='your_key',enable_caching=True,cache_timeout=50000)
Article=wrapy.WraPy('https://api.nytimes.com/svc/search/v2/articlesearch.json',main_args=['q'],argmap={'api_key':'api-key'},api_key='blah')
HTTPCat=wrapy.WraPy('https://http.cat/',api_type='url',arg_count=1)
HTTPBin=wrapy.WraPy('http://httpbin.org/',num_retries=0,arg_count=1,api_type='url',arg_default=['get'],)
@ArchivedArticle.function
def __repr__(self):
    return 'My Pretty Article'
@ArchivedArticle.function
def resp(self):
    return self.response
@ArchivedArticle.function
def __getitem__(self,i):
    return self.response.docs[i]
@ArchivedArticle.response
def returnself(self):
    return self
@ArchivedArticle.response.docs
def hello(self):
    return 'Document'
