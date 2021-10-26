import wrapy

group=wrapy.WraPyGroup(api_type='combined',argmap={'api_key':'api-key'},api_key='yourkey')
ArchivedArticle=group.WraPy('https://api.nytimes.com/svc/archive/v1/',root_url_fstring='{}.json',arg_count=2)
Article=group.WraPy('https://api.nytimes.com/svc/search/v2/articlesearch.json',main_args=['q'])
