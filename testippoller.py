import unittest
import unittest.mock
from ippoller import DynDnsProvider


class TestDynDnsResponse(unittest.TestCase):

    class ResponseStub:

        def read(self, length):
            return  b'<html><head><title>Current IP Check</title></head><body>' \
                b'Current IP Address: 192.168.1.10</body></html>\r\n'


    @unittest.mock.patch('http.client.HTTPConnection.request')
    @unittest.mock.patch('http.client.HTTPConnection.getresponse', return_value=ResponseStub())
    def test_parsing(self, mock_getresponse, mock_request):
        provider = DynDnsProvider()
        self.assertEqual("192.168.1.10", provider.getIP())
        mock_request.assert_called_once_with('GET', '/')
        mock_getresponse.assert_called_once_with()


