#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError
try:
    from pycomm3 import LogixDriver
    HAS_PYCOMM3 = True
except ImportError:
    HAS_PYCOMM3 = False

class LogixUtil(object):

    def __init__(self, module):
        if not HAS_PYCOMM3:
            self.module.fail_json("Python module pycomm3 required for industrial.logix")

        # Setup logging for format, set log level and redirect to string
        self.module = module
        self.connection = Connection(self.module._socket_path)
        self.logix_address = self.connection.get_option('host')
        import q; q.q(self.connection.host)
        self.plc = LogixDriver(self.logix_address)

    def get_tags(self):
        return self.plc.tags


