import unittest
import wrapy
import warnings
warnings.filterwarnings("ignore")
class TestWraPyJSON(unittest.TestCase):
    def test_json(self):
        wrapy.WraPy('https://randomuser.me/api/')
class TestWraPyXML(unittest.TestCase):
    def test_xml(self):
        wrapy.WraPyObject('https://nominatim.openstreetmap.org/search',num_retries=24,q='berlin',format='xml')
class TestWraPyRaisesNotWellFormed(unittest.TestCase):
    def test_raises_not_well_formed(self):
        self.assertRaises(wrapy.EndpointError,wrapy.WraPyObject,'https://google.com/')
class TestWraPyRaisesHTTPError(unittest.TestCase):
    def test_raises_http(self):
        self.assertRaises(wrapy.HTTPError,wrapy.WraPyObject,'https://api.agify.io/')

unittest.main()
