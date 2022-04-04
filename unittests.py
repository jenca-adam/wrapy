import shutil 
try:
    shutil.rmtree('.cache/wrapy')
except:pass
import unittest
import wrapy
import warnings
import shutil
import timeit

warnings.filterwarnings("ignore")
class TestWraPyJSON(unittest.TestCase):
    def test_json(self):
        wrapy.WraPyObject('https://randomuser.me/api/')
class TestWraPyXML(unittest.TestCase):
    def test_xml(self):
        wrapy.WraPyObject('https://nominatim.openstreetmap.org/search',num_retries=24,q='berlin',format='xml')
class TestWraPyRaisesNotWellFormed(unittest.TestCase):
    def test_raises_not_well_formed(self):
        self.assertRaises(wrapy.EndpointError,wrapy.WraPyObject,'https://google.com/')
class TestWraPyRaisesHTTPError(unittest.TestCase):
    def test_raises_http(self):
        self.assertRaises(wrapy.HTTPError,wrapy.WraPyObject,'https://api.agify.io/')
class TestWraPyImage(unittest.TestCase):
    def test_image(self):
        wrapy.WraPy('https://http.cat/',api_type='url',arg_count=1)(404)
class TestWraPyCache(unittest.TestCase):
    def test_cache(self):
        global x
        x=wrapy.WraPy('https://nominatim.openstreetmap.org/search',num_retries=24,format='xml',enable_caching=True)
        tx=timeit.timeit('x(q="berlin")',number=1,globals=globals())
        tx2=timeit.timeit('x(q="berlin")',number=1,globals=globals())
        self.assertGreater(tx,tx2)
class TestWraPyPost(unittest.TestCase):
    def test_post_form(self):
        x=wrapy.WraPy('http://httpbin.org/post',api_type='post')
        tx=x(abcd='efgh')

unittest.main()
