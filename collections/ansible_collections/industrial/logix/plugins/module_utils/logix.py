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
        ping = module.get_bin_path("ping")
        rc, stdout, stderr = module.run_command(
            [ping, self.logix_address.split('/')[0], '-c', '1']
        )
        if rc != 0:
            self.module.fail_json(
                msg="Unable to make connection to ControlLogix device: %s" % self.logix_address
            )

        self.plc = LogixDriver(self.logix_address)

