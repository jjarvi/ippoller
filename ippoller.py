import http.client
import re
import time


class DynDnsProvider:

    url = "checkip.dyndns.org"

    def get_ip(self):
        conn = http.client.HTTPConnection(self.url)
        conn.request("GET", "/")
        maxlen = 512
        return self._parse_ip_from_response(conn.getresponse().read(maxlen).decode())

    def _parse_ip_from_response(self, response):
        match = re.search('Address:\ ([\d\.]+)', response)
        return match.group(1) if match and len(match.groups()) == 1 else ''



class IpPoller:

    def __init__(self, provider, on_ip_changed_cb):
        self.provider = provider
        self.period_sec = 60 * 30
        self.running = True
        self.known_ip = None
        self.on_ip_changed_cb = on_ip_changed_cb

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            ip = self.provider.get_ip()
            self._check_if_ip_changed(ip)
            time.sleep(self.period_sec)

    def _check_if_ip_changed(self, ip):
        if self.known_ip == None:
            self.known_ip = ip
        elif ip != self.known_ip:
            self.on_ip_changed_cb(ip, self.known_ip)
            self.known_ip = ip


def on_ip_changed(new_ip, previous_ip):
    print('IP changed from {} to {}'.format(previous_ip, new_ip))

if __name__ == '__main__':
    IpPoller(DynDnsProvider(), on_ip_changed)
