#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError


class LogixUtil(object):

    def __init__(self, module):

        # Setup logging for format, set log level and redirect to string
        self.module = module
        self.connection = Connection(self.module._socket_path)

    def get_tags(self):
        return self.connection.call_logix_action("tags")


