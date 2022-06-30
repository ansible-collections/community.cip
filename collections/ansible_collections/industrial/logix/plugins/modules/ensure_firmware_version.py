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
module: ensure_firmware_version
short_description: Ensure a tag has a specific value
description:
    - Ensure a tag has a specific value
author:
- Adam Miller (@maxamillion)
options:
  name:
    description:
      - Name of the tag to target
    required: true
    type: str
  value:
    description:
      - Value to ensure the tag is set to.
      - This value is always a string in the playbook and will by typecast
        accordingly 
    required: true
    type: str
"""

EXAMPLES = """
- name: Ensure a tag is set
  industrial.logix.ensure_tag:
    name: LED
    value: True
  register: list_tags_out

- debug: var=list_tags_out
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

    argspec = dict(
        name=dict(required=True, type="str"),
        value=dict(required=True, type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)
    tag_name = module.params['name']
    tag_value = module.params['value']

    results = {}
    results['previous_value'] = ""
    if tag_name in logix_util.plc.tags:
        results['previous_value'] = logix_util.plc.read(tag_name).value
    else:
        module.fail_json(msg="ERROR: Tag %s not found" % tag_name)

    if str(logix_util.plc.read(tag_name).value).lower() == tag_value.lower():
        # FIXME - do this check .... better?
        module.exit_json(msg="Tag already set, no change needed", changed=False)

    # FIXME - Need to clean this up later, but it's fine for PoC
    plc_data_type = logix_util.plc.read(tag_name).type

    if plc_data_type == 'BOOL':
        tag_value = tag_value.lower() in ['true', '1', 't', 'y', 'yes']
    elif plc_data_type == 'REAL' or plc_data_type == 'FLOAT':
        tag_value = float(tag_value)
    elif plc_data_type == 'DINT' or plc_data_type == 'DINT':
        tag_value = int(tag_value)

    write_result = logix_util.plc.write((tag_name, tag_value))

    if not bool(write_result):
        logix_util.module.fail_json('Failed to write tag')

    results['data_type'] = plc_data_type
    results['value'] = tag_value
    results['write_result'] = write_result

    module.exit_json(msg="Updated tag", changed=True, results=results)

if __name__ == "__main__":
    main()
