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
module: verify_cip_security
short_description: Verify CIP Security is available and/or enabled
description:
  - Verify CIP Security is available, which security profiles and are they configured
author:
  - Matthew Sandoval (@matoval)
"""

EXAMPLES = """
- name: Verify CIP Security
  community.cip.verify_cip_security:
  register: cip_security

- name: Debug
  ansible.builtin.debug:
    var: cip_security
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.cip.plugins.module_utils.logix import LogixUtil


def main():
    module = AnsibleModule(argument_spec=dict(), supports_check_mode=True)

    logix_util = LogixUtil(module)

    all_available_attr = logix_util.plc.generic_message(
        service=logix_util.cip.Services.get_attribute_single,
        class_code=0x5D,
        instance=0,
        attribute=0,
        data_type=logix_util.cip.UINT,
    )  # noqa yaml[line-length]

    msg = []

    if "Destination unknown" in str(all_available_attr[3]):
        msg.append("CIP Security is unsupported")
    else:
        msg.append("CIP Security is supported")

        profiles = logix_util.plc.generic_message(
            service=logix_util.cip.Services.get_attribute_single,
            class_code=0x5D,
            instance=1,
            attribute=2,
            data_type=logix_util.cip.WORD,
            name="Security Profiles",
        )

        configured = logix_util.plc.generic_message(
            service=logix_util.cip.Services.get_attribute_single,
            class_code=0x5D,
            instance=1,
            attribute=3,
            data_type=logix_util.cip.WORD,
            name="Security Profiles Configured",
        )

        security_profiles = {
            0: "Reserved",
            1: "EtherNet/IP Confidentiality Profile",
            2: "CIP Authorization Profile",
            3: "CIP User Authentication Profile",
            4: "Resource-Constrained CIP Security Profile",
            5: "EtherNet/IP Pull Model Profile",
            **{i: "Reserved" for i in range(6, 15)},
        }

        for i in range(15):
            msg.append(
                f'Security profile - {security_profiles[i]}: {"not " if not profiles[1][i] else ""}available and {"not " if not configured[1][i] else ""}configured'  # noqa yaml[line-length]
            )

    module.exit_json(msg=msg)


if __name__ == "__main__":
    main()
