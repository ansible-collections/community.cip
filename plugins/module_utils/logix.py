#!/usr/bin/python

import atexit
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError
try:
    from pycomm3 import LogixDriver, cip
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
        self.cip = cip

        self.plc = LogixDriver(self.logix_address)

        try: 
            self.plc.open()
        except Exception as error:
            self.module.fail_json("Failed to open ControlLogix device %s, returned error message: (%s) Make sure this host is a PLC." % (self.logix_address, error))

        
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

    def parse_status_to_binary(self, status):
        reorder_hex = status.hex()[2:4] + status.hex()[0:2]
        convert_to_binary = bin(int(reorder_hex, 16))
        format_to_bit_identity_object = convert_to_binary[2:].zfill(16)
        return format_to_bit_identity_object

    def parse_status_to_text(self, binary_status):
        status = {} 
        mode = {
            0: "Self-Testing or Unknown",
            1: "Firmware Update in Progress",
            2: "At least one faulted I/O connection",
            3: "No I/O connections established",
            4: "Non-Volatile Configuration bad",
            5: "Major Fault",
            6: "At least one I/O connection in run mode",
            7: "At least one I/O connection established, all in idle mode",
            8: "The Status attribute is not applicable to this instance. Valid only for instances greater than one (1).",
            9: "Reserved",
            **{i: "Vendore specific" for i in range(10, 16)}
        }

        keyswitch = {
            0: "Unknown - not supported",
            1: "Mode Transitioning",
            2: "Test Mode",
            3: "Remote Mode"
        }

        status['owned'] = bool(int(binary_status[15]))
        status['configured'] = bool(int(binary_status[13]))
        status['mode'] = mode[int(binary_status[8:12], 2)]
        status['minor_recoverable_fault'] = bool(int(binary_status[7]))
        status['minor_unrecoverable_fault'] = bool(int(binary_status[6]))
        status['major_recoverable_fault'] = bool(int(binary_status[5]))
        status['major_unrecoverable_fault'] = bool(int(binary_status[4]))
        status['keyswitch'] = keyswitch[int(binary_status[2:4], 2)]
        status['transitioning'] = bool(int(binary_status[1]))
        status['debug'] = bool(int(binary_status[0]))

        return status
