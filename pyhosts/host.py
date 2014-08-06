import platform
from netaddr import IPAddress
from netaddr.core import AddrFormatError


class Host(object):
    def __init__(self, ipaddress, hostname, aliases, comments):
        self.ipaddress = Host._ipaddress(ipaddress)
        self.hostname = hostname
        self.aliases = aliases.split() if aliases else None
        self.comments = comments

    @staticmethod
    def _ipaddress(ipaddress):
        return IPAddress(ipaddress)

    def __str__(self):
        return str({'ipaddress': self.ipaddress,
                    'hostname': self.hostname,
                    'aliases': self.aliases,
                    'comments': self.comments})

    __repr__ = __str__

    def __bool__(self):
        if not self.ipaddress and \
                not self.hostname and \
                not self.aliases and \
                not self.comments:
            return False
        return True

    __nonzero__ = __bool__

    def __eq__(self, host):
        return (self.ipaddress == host.ipaddress and
                self.hostname == host.hostname and
                self.aliases == host.aliases)
