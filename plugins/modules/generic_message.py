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
    - A thin abstraction of the pycomm3 generic_message() API call. Connection related arguments are handled by ansible.
      This is intended for experienced developers needing functionality not already covered by the industrial.logix 
      plugin. The functionality of this module is similar to crafting a TCP packet by hand. Typically, this call uses 
      many builtin constants provided by the pycomm3 package, but in this case raw hex or dec values must be used. The
      lookup tables used by pycomm3 can be found in the following directory 
      https://github.com/ottowayi/pycomm3/tree/master/pycomm3/cip

author:
- Aaron Neustedter (@aaron97neu)
options:
  service:
    description:
      - service code for the request (single byte)
    required: True
    type: str
  class_code:
    description:
      - request object class ID
    required: True
    type: str
  instance:
    description:
      - ID for an instance of the class. If set to 0, request class attributes
    required: True
    type: str
  attribute:
    description:
      - attribute ID for the service/class/instance
    required: False
    default: b''
    type: str
  request_data:
    description: 
      - any additional data required for the request
    required: False
    default: None
    type: str
  data_type:
    description: 
      - dict containing description of the expected return data type
    required: False
    default: None
    type: dict
    options:
      elementary_type:
        description: elementary data type, choices described here https://docs.pycomm3.dev/en/latest/api_reference/data_types.html#pycomm3.cip.data_types.DataTypes
        required: True
        type: str
      array_len:
        description: If the data type if an array, the length of the array. Values less than 2 denote datatype is not an array
        type: int
        required: False
        default: 1
  name:
    description:
      - return Tag.Tag value, arbitrary but can be for tracking returned Tags
    required: False
    default: 'generic'
    type: str

"""

EXAMPLES = """
- name: Get MAC address of EN2T device
  industrial.logix.generic_message:
    service: 0x0E
    class_code: 0xF6
    instance: 1
    attribute: 3
    data_type:
      elementary_type: USINT
      array_len: 6

- name: Find the IP Setting configuration type. 0b_0000 = 'static', 0b_0001 = 'BOOTP' 0b_0010 = 'DHCP'
  industrial.logix.generic_message:
    service: 0x0E
    class_code: 0xf5
    instance: 1
    attribute: 3
    data_type:
      elementary_type: INT
      array_len: -1
    name: 'IP_config'
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil

from pycomm3 import data_types, DataTypes

def main():

    dtspec = dict(
        elementary_type=dict(required=True, type="str"),
        array_len=dict(required=False, default = 1, type="int"),
      )

    argspec = dict(
        service=dict(required=True, type="str"),
        class_code=dict(required=True, type="str"),
        instance=dict(required=True, type="str"),
        attribute=dict(required=False, default=b'', type="str"),
        request_data=dict(required=False, default=None, type="str"),
        data_type=dict(required=False, default=None, type="dict", options=dtspec),
        name=dict(required=False, default=None, type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    # coerce data_type from a description of the data type to the actual object. This is gonna be messy
    dt_arg = module.params['data_type']
    data_type = None
    if dt_arg is not None:
        if DataTypes.get(dt_arg['elementary_type']) is None:
            module.fail_json(f'elementart_type {dt_arg["elementary_type"]} is not one of allowed data types: {DataTypes.attributes}')
        
        if dt_arg['array_len'] > 1:
            data_type = data_types.Array(element_type_=DataTypes.get(dt_arg['elementary_type']), length_=dt_arg['array_len'])
        else:
            data_type = DataTypes.get(dt_arg['elementary_type'])
    
    # request_data expects a bits-like object, so None (if no argument is supplied) needs to be converted
    request_data = module.params['request_data']
    if request_data == None:
        request_data = b''

    ret = logix_util.plc.generic_message(
        service = int(module.params['service'], 0), # int(something, 0) -> https://stackoverflow.com/a/21669474
        class_code = int(module.params['class_code'], 0),
        instance = int(module.params['instance'], 0),
        attribute = int(module.params['attribute'], 0),
        request_data = bytes(int(request_data, 0)),
        data_type = data_type,
        name = module.params['name'],
        connected = False, # TODO: Double check all connection stuff
        unconnected_send = False,
        route_path= False
    )

    module.exit_json(msg=f'{ret}', changed=False)


if __name__ == "__main__":
    main()
