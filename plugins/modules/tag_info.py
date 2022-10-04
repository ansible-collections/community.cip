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
module: tag_info
short_description: Pull information about current tags as set on the ControlLogix
description:
  - Info module to get a list of blueprints from Weldr
author:
- Adam Miller (@maxamillion)
"""

EXAMPLES = """
- name: Get list of tags
  community.cip.tag_info:
  register: list_tags_out

- debug: var=list_tags_out
"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.community.cip.plugins.module_utils.logix import LogixUtil


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True
    )

    logix_util = LogixUtil(module)

    module.exit_json(tags=logix_util.plc.tags_json, msg="Tag information gathered.")


if __name__ == "__main__":
    main()
