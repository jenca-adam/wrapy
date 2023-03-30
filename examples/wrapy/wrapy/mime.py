import re
import mimetypes
from .unique import *
_JSON_PATTERN=re.compile('.*/.*json.*')
_XML_PATTERN=re.compile('xml')
_IMAGE_PATTERN=re.compile('^image/.*')
class InvalidMIMEError(Exception):pass
class MimeTypes:
    JSON=Unique()
    XML=Unique()
    IMAGE=Unique()
    UNKNOWN=Unique()

def independent_header(d,headername):
    if hasattr(d,'getheader'):
        return d.getheader(headername)
    if hasattr(d,'headers'):
        return d.headers[headername]
    return d[headername.lower()]
def mime(j):
    if j not in mimetypes.types_map.values():
        raise InvalidMIMEError(f'invalid MIME type: {j!r}')
    if _JSON_PATTERN.match(j):
        return MimeTypes.JSON
    elif 'xml' in j:
        return MimeTypes.XML
    elif _IMAGE_PATTERN.match(j):
        return MimeTypes.IMAGE
    else:
        return MimeTypes.UNKNOWN
def detect(d):
    return mime(independent_header(d,'Content-Type').split(';')[0])
