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
    - A thin abstraction of the pycomm3 generic_message() API call. Connection
      related arguments are handled by ansible.
    - This is intended for experienced developers needing functionality not
      already covered by the plugin. Think similar to crafting a TCP packet by
      hand. Typically, this call uses many builtin constants provided by the
      pycomm3 package, but in this case raw hex or dec values must be used.
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
    default: ""
    type: str
  request_data:
    description:
      - any additional data required for the request
    required: False
    default: ""
    type: str
  data_type:
    description:
      - dict containing discription of the expected return data type
    required: False
    default: {}
    type: dict
    suboptions:
      elementary_type:
        description:
          - elementary data type, choices described here -
            https://docs.pycomm3.dev/en/latest/api_reference/data_types.html#pycomm3.cip.data_types.DataTypes
        required: True
        type: str
      array_len:
        description:
          - If the data type if an array, the length of the array. Values less
            than 2 denote datatype is not an array
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
from ansible.module_utils._text import to_native, to_text, to_bytes
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil
from ansible.module_utils.basic import missing_required_lib

import traceback
try:
    from pycomm3 import data_types, DataTypes
except ImportError:
    HAS_PYCOMM3 = False
    PYCOMM3_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PYCOMM3 = True


def main():

    dtspec = dict(
        elementary_type=dict(required=True, type="str"),
        array_len=dict(required=False, default=1, type="int"),
    )

    argspec = dict(
        service=dict(required=True, type="str"),
        class_code=dict(required=True, type="str"),
        instance=dict(required=True, type="str"),
        attribute=dict(required=False, default="", type="str"),
        request_data=dict(required=False, default="", type="str"),
        data_type=dict(
            required=False, default=None, type="dict", options=dtspec
        ),
        name=dict(required=False, default="generic", type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    if not HAS_PYCOMM3:
        logix_util.module.fail_json(
            msg=missing_required_lib('pycomm3'),
            exception=PYCOMM3_IMPORT_ERROR)

    # coerce data_type from a description of the data type to the actual
    # object. This is gonna be messy
    dt_arg = module.params["data_type"]
    data_type = None
    if dt_arg is not None:
        if DataTypes.get(dt_arg["elementary_type"]) is None:
            module.fail_json(
                f'elementart_type {dt_arg["elementary_type"]} is not one of',
                f' allowed data types: {DataTypes.attributes}'
            )

        if dt_arg["array_len"] > 1:
            data_type = data_types.Array(
                element_type_=DataTypes.get(dt_arg["elementary_type"]),
                length_=dt_arg["array_len"],
            )
        else:
            data_type = DataTypes.get(dt_arg["elementary_type"])

    # request_data expects a bits-like object, so None (if no argument is supplied) needs to be converted
    request_data = module.params["request_data"]
    if not request_data:
        request_data = b""

    ret = logix_util.plc.generic_message(
        service=int(
            module.params["service"], 0
        ),  # https://stackoverflow.com/a/21669474
        class_code=int(module.params["class_code"], 0),
        instance=int(module.params["instance"], 0),
        attribute=int(to_bytes(module.params["attribute"]), 0),
        request_data=bytes(int(request_data, 0)),
        data_type=data_type,
        name=module.params["name"],
        connected=False,  # TODO: Double check all connection stuff
        unconnected_send=False,
        route_path=False,
    )

    module.exit_json(msg=f"{ret}", changed=False)


if __name__ == "__main__":
    main()
