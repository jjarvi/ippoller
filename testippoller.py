import unittest
import unittest.mock
from ippoller import DynDnsProvider, IpPoller

class TestDynDnsResponse(unittest.TestCase):

    class ResponseStub:

        def read(self, length):
            return  b'<html><head><title>Current IP Check</title></head><body>' \
                b'Current IP Address: 192.168.1.10</body></html>\r\n'


    @unittest.mock.patch('http.client.HTTPConnection.request')
    @unittest.mock.patch('http.client.HTTPConnection.getresponse', return_value=ResponseStub())
    def test_parsing(self, mock_getresponse, mock_request):
        provider = DynDnsProvider()
        self.assertEqual("192.168.1.10", provider.get_ip())
        mock_request.assert_called_once_with('GET', '/')
        mock_getresponse.assert_called_once_with()


class TestIpPoller(unittest.TestCase):

    def setUp(self):
        self.num_rounds = 0
        self.num_rounds_to_run = 1
        self.ip_to_return = '192.168.1.10'
        self.on_ip_changed_cb = unittest.mock.MagicMock()
        self.poller = IpPoller(self, self.on_ip_changed_cb)

    def get_ip(self):
        self.num_rounds += 1
        if self.num_rounds == self.num_rounds_to_run:
            self.poller.stop()
            self.num_rounds = 0
        return self.ip_to_return

    @unittest.mock.patch('time.sleep')
    def test_request_is_sent_periodically(self, mock_sleep):
        expected_period_in_seconds = 60 * 30
        self.num_rounds_to_run = 3
        self.poller.run()
        self.assertEqual([unittest.mock.call(expected_period_in_seconds),
                          unittest.mock.call(expected_period_in_seconds),
                          unittest.mock.call(expected_period_in_seconds)],
                         mock_sleep.mock_calls)

    @unittest.mock.patch('time.sleep')
    def test_ip_change(self, _):
        first_ip = '192.168.1.10'
        second_ip = '192.168.1.20'
        self.ip_to_return = first_ip
        self.poller.run()
        self.on_ip_changed_cb.assert_not_called()
        self.poller.run()
        self.on_ip_changed_cb.assert_not_called()
        self.ip_to_return = second_ip
        self.poller.run()
        self.on_ip_changed_cb.assert_called_once_with(second_ip, first_ip)
