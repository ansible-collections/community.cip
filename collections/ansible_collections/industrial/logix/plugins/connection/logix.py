from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#FIXME - I'm not sure we should do the backplane and slot vars
DOCUMENTATION = """
---
author: Ansible Edge Automation Team <https://github.com/ansible-edge>
connection: industrial.logix.logix
short_description: Plugin to directly interact with Rockwell Allen-Bradley ControlLogix
description:
  - This connection plugin provides a connection to Rockwell Allen-Bradley
    ControlLogix via the C(pycomm3) python library.
options:
  host:
    type: str
    description:
      - Specifies the remote device IP address of the ControlLogix
        to establish a connection to.
      - Notation can be IP Adress alone, "192.168.100.100" and slot 0 will be assumed.
        Alternatively the slot can be provided as IPAddress/SlotNumber, "192.168.100.100/3".
    default: inventory_hostname
    vars:
      - name: ansible_host
  persistent_connect_timeout:
    type: int
    description:
      - Configures, in seconds, the amount of time to wait when trying to
        initially establish a persistent connection.  If this value expires
        before the connection to the remote device is completed, the connection
        will fail.
    default: 30
    ini:
      - section: persistent_connection
        key: connect_timeout
    env:
      - name: ANSIBLE_PERSISTENT_CONNECT_TIMEOUT
    vars:
      - name: ansible_connect_timeout
  persistent_command_timeout:
    type: int
    description:
      - Configures, in seconds, the amount of time to wait for a command to
        return from the remote device.  If this timer is exceeded before the
        command returns, the connection plugin will raise an exception and
        close.
    default: 30
    ini:
      - section: persistent_connection
        key: command_timeout
    env:
      - name: ANSIBLE_PERSISTENT_COMMAND_TIMEOUT
    vars:
      - name: ansible_command_timeout
  persistent_log_messages:
    type: boolean
    description:
      - This flag will enable logging the command executed and response received from
        target device in the ansible log file. For this option to work 'log_path' ansible
        configuration option is required to be set to a file path with write access.
      - Be sure to fully understand the security implications of enabling this
        option as it could create a security vulnerability by logging sensitive information in log file.
    default: False
    ini:
      - section: persistent_connection
        key: log_messages
    env:
      - name: ANSIBLE_PERSISTENT_LOG_MESSAGES
    vars:
      - name: ansible_persistent_log_messages
"""

from io import BytesIO
import importlib

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.urls import open_url
from ansible.playbook.play_context import PlayContext
from ansible.plugins.connection import NetworkConnectionBase, ensure_connect

try:
    from pycomm3 import LogixDriver
    HAS_PYCOMM3 = True
except ImportError:
    HAS_PYCOMM3 = False


class Connection(NetworkConnectionBase):
    '''Rockwell Allen-Bradley ControlLogix via pycomm3 library connection'''

    transport = 'logix'
    has_pipelining = False
    has_tty = False

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)

        if not HAS_PYCOMM3:
            raise AnsibleConnectionFailure(
                "Error> python pycomm3 module required for industrial.logix.logix connection plugin"
            )

    def _connect(self):
        if not self.connected:
            host = self.get_option('host')

            plc = LogixDriver(host)
            self._sub_plugin = {
                'type': 'network',
                'name': 'logix',
                'obj': plc
            }
            self._connected = True

            self.queue_message(
                'vvv',
                "Connection to ControlLogix established: %s" % host
            )

    def call_logix_action(self, attribute, options={}):
        """
        Imports a module and executes a target module dynamically using the
        persistent LogixDriver instance.

            :arg attribute: str, the pycomm3.LogixDriver attribute to call
            :arg options: dict, the dict of options to pass to the API call

            :returns: dict, return value(s) from the api call
        """
        try:
            self.queue_message('vvv', 'Action method to be imported from module: ' + attribute)
            self.queue_message('vvv', 'Action method name is: ' + attribute)

            with LogixDriver(self.get_option('host')) as plc:

                if hasattr(plc, attribute):
                    func_ptr = getattr(plc, attribute)  # Convert action to actual function pointer
                else:
                    raise AnsibleConnectionFailure("Error> Attempt was made execute an invalid pycomm3.ControlLogix attribute")
                if callable(func_ptr):
                    if options:
                        func_call = 'func_ptr(' + options + ')'
                    else:
                        func_call = 'func_ptr()'
                else:
                    # This is an attribute, not a function/method
                    func_call = "plc.%s" % attribute

            # Execute requested 'action'
            ret_obj = eval(func_call)
            #ret_obj['ansible_facts'] = plc.facts #FIXME - facts?
            return ret_obj
        except ImportError as e:
            raise AnsibleConnectionFailure('Error> action belongs to a module that is not found!', attribute, e)
        except AttributeError as e:
            raise AnsibleConnectionFailure('Error> invalid action was specified, method not found in module!', attribute, e)
        except TypeError:
            raise AnsibleConnectionFailure(
                'Error> action does not have the right set of arguments or there is a code bug! Options: ' + options,
                attribute,
                e
            )

    def close(self):
        '''
        Close the active session to the device
        '''
        # only close the connection if its connected.
        if self._connected:
            self.queue_message('vvv', "closing connection to ControlLogix device")

        super(Connection, self).close()

