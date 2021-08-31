import http.client
import re


class DynDnsProvider:

    url = "checkip.dyndns.org"

    def getIP(self):
        conn = http.client.HTTPConnection(self.url)
        conn.request("GET", "/")
        maxlen = 512
        return self._parse_ip_from_response(conn.getresponse().read(maxlen).decode())

    def _parse_ip_from_response(self, response):
        match = re.search('Address:\ ([\d\.]+)', response)
        return match.group(1) if match and len(match.groups()) == 1 else ''


def main():
    provider = DynDnsProvider()
    print(provider.getIP())


if __name__ == '__main__':
    main()

