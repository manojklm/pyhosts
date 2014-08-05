import unittest
from nose.tools import nottest
from mock import MagicMock

from pyhosts import Hosts, Host

from netaddr import IPAddress


class TestBaseCases(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.myhosts = Hosts()

    def test_one(self):
        self.assertEquals("/etc/hosts", self.myhosts.file_path)

    def test_readlines(self):
        self.assertEqual(4, len([i for i in self.myhosts]))

    def test_content_empty(self):
        self.myhosts._readlines = lambda x: []

        entries = [i for i in self.myhosts]
        expected = []
        self.assertEquals(expected, entries)

    def test_content_one_entry(self):
        self.myhosts._readlines = lambda x: ['127.0.0.1\t\tlocalhost.localdomain localhost\n',]

        entries = self.myhosts._rows()
        expected = [Host('127.0.0.1', 'localhost.localdomain', 'localhost', None)]
        self.assertEquals(expected, entries)

    def test_content_many_entries(self):
        self.myhosts._readlines = lambda x: ['127.0.0.1\t\tlocalhost.localdomain localhost\n', '::1\t\tlocalhost6.localdomain6 localhost6\n', '\n', '172.19.29.156\tigor\n', '\n', '# virtual machines\n', '192.168.122.167\tmarev3\n']

        entries = [host for host in self.myhosts]
        expected = [Host('127.0.0.1', 'localhost.localdomain', 'localhost', None),
                    Host('::1', 'localhost6.localdomain6', 'localhost6', None),
                    Host('172.19.29.156', 'igor', None, None),
                    Host('192.168.122.167', 'marev3', None, None)]

        self.assertEquals(expected, entries)

    def test_read_host(self):
        self.myhosts._readlines = lambda x: ['1.1.1.1\tigor',]
        self.assertEquals(IPAddress('1.1.1.1'), self.myhosts.igor.ipaddress)
        self.assertEquals('igor', self.myhosts.igor.hostname)
