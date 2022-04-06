try:
    import inflect
except ImportError:
    from . import simplu as inflect
engine=inflect.engine()
def plural(word):
    if word.endswith('s'):
        return word
    return engine.plural(word)
def singular(word):
    if not word.endswith('s'):
        return word
    return engine.singular_noun(word)
