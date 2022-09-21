#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Red Hat Inc.
# MIT (see COPYING or https://opensource.org/licenses/MIT)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: generic_message
short_description: Craft and send a custom "generic" CIP message
description:
    - A thin abstraction of the pycomm3 generic_message API call. Connection related arguments are handled by ansible.
      This is intended for experienced developers needing functionality not already covered by the plugin. Think similar
      to crafting a TCP packet by hand
author:
- Aaron Neustedter (@aaron97neu)
options:
  service:
    description:
      - service code for the request (single byte)
      required: True
      type: Union[int, bytes]
  class_code:
    description:
      - request object class ID
      required: True
      type: Union[int, bytes]
  instance:
    description:
      - ID for an instance of the class. If set to 0, request class attributes
      required: True
      type: Union[int, bytes]
  attribute:
    description:
      - attribute ID for the service/class/instance
      required: False
      default: b''
      type: Union[int, bytes]
  request_data:
    description: 
      - any additional data required for the request
      required: False
      default: b''
      type: any
  data_type:
    description: 
      - a DataType class (enumerated here: ___) that will be used to decode the
        response. None will return bytes
      required: False
      default: None
      type: Union[Type[DataType], DataType, None]
  name:
    description:
      - return Tag.Tag value, arbitrary but can be for tracking returned Tags
      required: False
      default: 'generic'
      type: str

"""

EXAMPLES = """
- name: check major firmware revision
  industrial.logix.ensure_firmware_revision:
    revision: 33
- name: check major and minor firmware revision
  industrial.logix.ensure_firmware_revision:
    revision: 33.001
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

     
    argspec = dict(
        revision=dict(required=True, type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    ret = logix_util.plc.generic_message(
        service = module.params['service'],
        class_code = module.params['class_code'],
        instance = module.params['instance'],
        attribute = module.params['attribute'],
        request_data = module.params['request_data'],
        data_type = module.params['datatype'], # This will need to be fixed
        name = module.params['name'],
        connected = False, # Double check all this. We are following th pycomm3 docs examples
        unconnected_send = True,
        route_path= True
    )

    module.exit_json(f'Generic message returns: {ret}', changed=False)


if __name__ == "__main__":
    main()
