import wrapy
HTTPBin=wrapy.WraPy('http://httpbin.org/',num_retries=0,arg_count=1,api_type='url',arg_default=['get'],)
