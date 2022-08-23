#!/usr/bin/python

import atexit
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

        self.plc = LogixDriver(self.logix_address)
        self.plc.open()

        
        if not self.plc.connected:
            self.module.fail_json(
                "Unable to connect to ControlLogix device: %s" % self.logix_address
            )

        atexit.register(self.cleanup)

    def cleanup(self):
        self.plc.close()

    def typecast_plc_value(self, plc_data_type, tag_value):
        if plc_data_type == 'BOOL':
            tag_value = tag_value.lower() in ['true', '1', 't', 'y', 'yes']
        elif plc_data_type == 'REAL' or plc_data_type == 'FLOAT':
            tag_value = float(tag_value)
        elif plc_data_type == 'DINT' or plc_data_type == 'DINT':
            tag_value = int(tag_value)
        return tag_value
