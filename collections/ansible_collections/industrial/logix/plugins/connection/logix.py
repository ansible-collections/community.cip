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
    default: inventory_hostname
    vars:
      - name: ansible_host
  backplane:
    type: str
    description:
      - Specifies the Backplane to connect to
    ini:
      - section: defaults
        key: ansible_logix_backplane
    env:
      - name: ANSIBLE_LOGIX_backplane
    vars:
      - name: ansible_logix_slot
  slot:
    type: int
    description:
      - Specifies the port on the Backplane Slot to connect to.
    ini:
      - section: defaults
        key: ansible_logix_slot
    env:
      - name: ANSIBLE_LOGIX_SLOT
    vars:
      - name: ansible_logix_slot
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

        self.plc = None
        if not HAS_PYCOMM3:
            raise AnsibleConnectionFailure(
                "Error> python pycomm3 module required for industrial.logix.logix connection plugin"
            )

    def _connect(self):
        if not self.connected:
            host = self.get_option('host')

            self.plc = LogixDriver(host)
            self._sub_plugin = {'name': 'plc', 'obj': self.plc}
            self._connected = True

            self.queue_message(
                'vvv',
                "Connection to ControlLogix established: %s" % host
            )

    def call_logix_action(self, logix_module, options):
        """
        Imports a module and executes a target module dynamically using the
        persistent LogixDriver instance.

            :arg logix_module: str, the fully qualified module.method name to invoke
            :arg options: dict, the dict of options to pass to the API call

            :returns: dict, return value(s) from the api call
        """
        if not self.connected:
            self._connect()
        try:
            module_name, method_name = logix_module.rsplit('.', 1)
            self.queue_message('vvv', 'Action method to be imported from module: ' + module_name)
            self.queue_message('vvv', 'Action method name is: ' + method_name)
            mod = importlib.import_module(module_name)
            func_ptr = getattr(mod, method_name)  # Convert action to actual function pointer
            func_call = 'func_ptr(' + options + ')'

            # Execute requested 'action'
            ret_obj = eval(func_call)
            #ret_obj['ansible_facts'] = self.plc.facts #FIXME - facts?
            return ret_obj
        except ImportError as e:
            raise AnsibleConnectionFailure('Error> action belongs to a module that is not found!', logix_module, e)
        except AttributeError as e:
            raise AnsibleConnectionFailure('Error> invalid action was specified, method not found in module!', logix_module, e)
        except TypeError:
            raise AnsibleConnectionFailure(
                'Error> action does not have the right set of arguments or there is a code bug! Options: ' + options,
                logix_module,
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

