import wrapy

HTTPCat=wrapy.WraPy('https://http.cat/',api_type='url',arg_count=1)
@HTTPCat.function
def __repr__(self):
    return 'Naughty Kitten!'
