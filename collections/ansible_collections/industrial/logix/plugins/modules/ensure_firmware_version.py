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
  major_version:
    description:
      - Major firmware version to validate
    required: true
    type: int
  minor_version:
    description:
      - Minor firmware version to validate
    required: false
    type: int
"""

EXAMPLES = """
- name: check firmware version
  industrial.logix.ensure_firmware_version:
    major_version: 33
    minor_version: 01

"""


import os
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

    # Instead of needing two args, I would love if we could take a single 
    # major.minorand automagically figure out `major` or `major.*` or something
    # to signify that we are want to verify major version
     
    argspec = dict(
        major_version=dict(required=True, type="int"),
        minor_version=dict(required=False, type="int")
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    with logix_util.plc as plc:
        plc_version = plc.get_plc_info()['revision']

    # check major revision
    if plc_version['major'] != module.params['major_version']:
        module.fail_json(
            msg="Major version %s not confirmed. Major version %s found instead." % (
                module.params['major_version'], plc_version['major']
            )
        )

    # Do we need to check for minor version?
    if "minor_version" in module.params:
        # Check minor version
        if plc_version['minor'] != module.params['minor_version']:
            module.fail_json(
            msg="Major version %s confirmed but minor version %s not confirmed. Minor version %s found instead." % (
                module.params['major_version'], module.params['minor_version'], plc_version['minor']
            )
        )


    if "minor_version" in module.params:
        module.exit_json(
            msg="Version %s.%s confirmed." % (
                module.params['major_version'], module.params['minor_version']
            ),
            changed=False
        )
    else:
        module.exit_json(
            msg="Major version %s confirmed." % module.params['major_version'], changed=False
        )

if __name__ == "__main__":
    main()
