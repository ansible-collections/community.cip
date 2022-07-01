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
        self.module = module

        if not HAS_PYCOMM3:
            self.module.fail_json("Python module pycomm3 required for industrial.logix")

        self.connection = Connection(self.module._socket_path)
        self.logix_address = self.connection.get_option('host')

        # Sanity test
        with LogixDriver(self.logix_address) as plc:
            if not plc.connected:
                self.module.fail_json(
                    "Unable to connect to ControlLogix device: %s" % self.logix_address
                )
            self.plc = plc

