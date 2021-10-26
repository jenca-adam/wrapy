import wrapy

User=wrapy.WraPy('https://randomuser.me/api/')
Location=wrapy.WraPy('https://nominatim.openstreetmap.org/search/',num_retries=3,main_args=['q'],args_required=True,format='xml')
ArchivedArticle=wrapy.WraPy('https://api.nytimes.com/svc/archive/v1/',api_type='combined',root_url_fstring='{}.json',arg_count=2,argmap={'api_key':'api-key'},api_key='6EbhSPRBcbXSEoAvz2r7wkALp0R9zNbX')
Article=wrapy.WraPy('https://api.nytimes.com/svc/search/v2/articlesearch.json',main_args=['q'],argmap={'api_key':'api-key'},api_key='6EbhSPRBcbXSEoAvz2r7wkALp0R9zNbX')
