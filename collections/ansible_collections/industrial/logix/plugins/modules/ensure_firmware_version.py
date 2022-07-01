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
short_description: Ensure firmware is a specific version or fail
description:
    - Ensure firmware is a specific version or fail
author:
- Adam Miller (@maxamillion)
options:
  version:
    description:
      - Firmware version to validate
    required: true
    type: str
"""

EXAMPLES = """
- name: check firmware version
  industrial.logix.ensure_firmware_version:
    version: "1.2.3"

"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

    argspec = dict(
        version=dict(required=True, type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    if logix_util.plc.revision_major != module.params['version']:
        module.fail_json(
            msg="Version %s not confirmed. Version %s found instead." % (
                module.params['version'], logix_util.plx.revision_major
            )
        )

    module.exit_json(
        msg="Version %s confirmed." % module.params['version'], changed=False
    )

if __name__ == "__main__":
    main()
