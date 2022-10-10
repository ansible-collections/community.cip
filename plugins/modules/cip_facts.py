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
module: cip_facts
short_description: Gathers cip facts from plc
description:
    - Gathers cip facts from plc and inject them into ansible facts
author:
- Chris Santiago (@resoluteCoder)
"""

EXAMPLES = """
- name: Gather cip facts
  community.cip.cip_facts:
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.cip.plugins.module_utils.logix import LogixUtil


def main():

    argspec = dict(
    )

    module = AnsibleModule(argument_spec=argspec, supports_check_mode=True)

    logix_util = LogixUtil(module)

    cip_facts = {'cip': {}}
    status = logix_util.plc.info['status']
    binary_status = logix_util.parse_status_to_binary(status)
    status_text = logix_util.parse_status_to_text(binary_status)

    cip_facts['cip'] = logix_util.plc.info
    cip_facts['cip']['status'] = status_text

    module.exit_json(
        msg="cip facts gather", ansible_facts=cip_facts
    )


if __name__ == "__main__":
    main()
