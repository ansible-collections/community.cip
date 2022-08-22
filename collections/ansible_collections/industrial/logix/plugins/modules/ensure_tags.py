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
import q

class TagCheck:
    def __init__(self, logix_util, tag_name):
        self.logix_util = logix_util
        self.tag_name = tag_name
        self.passed = False
        self.msg = ''

    def check_tag_exists(self):
        response = self.logix_util.plc.read(self.tag_name)
        if response.error:
            raise Exception('Tag %s not found' % self.tag_name)

    def check_tag_permissions(self):
        tag_info = self.logix_util.plc.get_tag_info(self.tag_name)
        if tag_info['external_access'] != 'Read/Write':
            raise Exception('Tag %s does not have correct permissions' % self.tag_name)

    def verify(self):
        try:
            self.check_tag_exists()
            self.check_tag_permissions()
            return (True, self.msg)
        except Exception as e:
            self.msg = e
            return (self.passed, self.msg)


def parse_sequence(sequence):
    min, max = sequence.replace('[', '').replace(']', '').split(':')
    return (int(min), int(max))


def main():

    subopts = dict(
        name=dict(required=True, type="str"),
        value=dict(requied=True, type="str"),
    )

    argspec = dict(
        tags=dict(type="list", options=subopts, elements="dict"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)
    tags_results = {}
    has_changed = False

    for tag in module.params['tags']:
        tag_name = tag['name']
        tag_value = tag['value']

        tags_results[tag_name] = {}
        tags_results[tag_name]['previous_value'] = ""

        if ':' in tag_value:
            start, end = parse_sequence(tag_value)
            q.q(start, end)

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

        logix_util.typecast_plc_value(plc_data_type, tag_value)

        write_result = logix_util.plc.write((tag_name, tag_value))

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
