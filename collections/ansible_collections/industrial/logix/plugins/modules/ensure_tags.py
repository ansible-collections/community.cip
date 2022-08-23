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
module: ensure_tags
short_description: Ensure tags have a specific value
description:
    - Ensure tags have a specific value
author:
- Matthew Sandoval (@matoval)
options:
  tags:
    description:
      - List of tags with name and value
    required: true
    type: list
    elements: dict
    suboptions:
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
  industrial.logix.ensure_tags:
    tags:
      - name: LED
        value: True
  register: list_tags_out

- debug: var=list_tags_out
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil
from ansible_collections.industrial.logix.plugins.module_utils.tag_check import TagCheck
import q


def main():

    tag_options = dict(
        name=dict(required=True, type="str"),
        value=dict(requied=True, type="str"),
    )

    argspec = dict(
        program=dict(type="str", required=False),
        tags=dict(type="list", options=tag_options, elements="dict", required=True),
    )

    module = AnsibleModule(argument_spec=argspec)

    logix_util = LogixUtil(module)
    tags_results = {}
    has_changed = False

    for tag in module.params['tags']:
        if module.params['program']:
            tag_name = 'Program:%s.%s' % (module.params['program'], tag['name'])
        else:
            tag_name = tag['name']

        tag_value = tag['value']

        tags_results[tag_name] = {}
        tags_results[tag_name]['previous_value'] = ""

        tag_check = TagCheck(logix_util, tag_name)
        passed, msg = tag_check.verify()
        if not passed:
            module.fail_json(msg=msg)

        tags_results[tag_name]['previous_value'] = logix_util.plc.read(tag_name).value

        if str(logix_util.plc.read(tag_name).value).lower() == tag_value.lower():
            # FIXME - do this check .... better?
            tags_results[tag_name]['no_change_need'] = True
            continue

        # FIXME - Need to clean this up later, but it's fine for PoC
        plc_data_type = logix_util.plc.read(tag_name).type

        typecast_tag_value = logix_util.typecast_plc_value(plc_data_type, tag_value)
        # q.q(type())
        write_result = logix_util.plc.write(tag_name, typecast_tag_value)

        if not bool(write_result):
            logix_util.module.fail_json('Failed to write tag')


        tags_results[tag_name]['data_type'] = plc_data_type
        tags_results[tag_name]['value'] = tag_value
        tags_results[tag_name]['write_result'] = write_result
        if tags_results[tag_name]['write_result']:
            has_changed = True

    module.exit_json(msg="Tags values", changed=has_changed, ansible_module_results=tags_results)

if __name__ == "__main__":
    main()
