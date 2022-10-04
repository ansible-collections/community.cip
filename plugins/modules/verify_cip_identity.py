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
module: verify_cip_identity
short_description: Verify CIP identity of PLC
description:
    - Verify CIP identity of PLC
author:
- Matthew Sandoval (@matoval)
options:
  cip_identity:
    description:
      - Dictionary of status properties that are part of CIP Identitiy
    required: true
    type: dict
    suboptions:
      vendor_id:
        description:
          - Value is the vendor id of the plc.
        required: false
        type: int
      device_type:
        description:
          - Value is the device type of the plc.
        required: false
        type: int
      product_code:
        description:
          - Value is the product code of the plc.
        required: false
        type: int
      revision:
        description:
          - firmware revision to validate in the form XX.YYY
        required: false
        type: str
      status:
        description:
          - Value to ensure the tag is set to.
        required: false
        type: dict
        suboptions:
          owned:
            description:
              - Value indicating the plc has an owner.
            required: false
            type: bool
          configured:
            description:
              - Value indicating if the plc is configured different than the "out-of-box" default.
            required: false
            type: bool
          mode:
            description:
              - Value indicating the current mode of the plc.
            required: false
            type: str
          minor_recoverable_fault:
            description:
              - Value indicating if there is a minor recoverable fault.
            required: false
            type: bool
          minor_unrecoverable_fault:
            description:
              - Value indicating if there is a minor unrecoverable fault.
            required: false
            type: bool
          major_recoverable_fault:
            description:
              - Value indicating if there is a major recoverable fault.
            required: false
            type: bool
          major_unrecoverable_fault:
            description:
              - Value indicating if there is a major unrecoverable fault.
            required: false
            type: bool
          keyswitch:
            description:
              - Value indicating current keyswitch mode.
            required: false
            type: str
          transitioning:
            description:
              - Value indicating if status is currently transitioning.
            required: false
            type: bool
          debug:
            description:
              - Value indicating if debug mode is active.
            required: false
            type: bool
      serial_number:
        description:
          - Value is the serial number of the plc.
        required: false
        type: str
      product_name:
        description:
          - Value is the product name of the plc.
        required: false
        type: str
"""

EXAMPLES = """
- name: Verify CIP identity
  industrial.logix.verify_cip_identity:
    cip_identity:
      vendor_id: "{{ hostvars[inventory_hostname]['vendor_id'] }}"
      device_type: "{{ hostvars[inventory_hostname]['device_type'] }}"
      product_code: "{{ hostvars[inventory_hostname]['product_code'] }}"
      revision: "{{ hostvars[inventory_hostname]['revision'] }}"
      status:
        owned: "{{ hostvars[inventory_hostname]['owned'] }}"
        configured: "{{ hostvars[inventory_hostname]['configured'] }}"
        mode: "{{ hostvars[inventory_hostname]['mode'] }}"
        minor_recoverable_fault: "{{ hostvars[inventory_hostname]['minor_recoverable_fault'] }}"
        minor_unrecoverable_fault: "{{ hostvars[inventory_hostname]['minor_unrecoverable_fault'] }}"
        major_recoverable_fault: "{{ hostvars[inventory_hostname]['major_recoverable_fault'] }}"
        major_unrecoverable_fault: "{{ hostvars[inventory_hostname]['major_unrecoverable_fault'] }}"
        keyswitch: "{{ hostvars[inventory_hostname]['keyswitch'] }}"
        transitioning: "{{ hostvars[inventory_hostname]['transitioning'] }}"
        debug: "{{ hostvars[inventory_hostname]['debug'] }}"
      serial_number: "{{ hostvars[inventory_hostname]['serial_number'] }}"
      product_name: "{{ hostvars[inventory_hostname]['product_name'] }}"
  register: ensure_firmware_version_out

- debug: var=ensure_firmware_version_out
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

    statusopt = dict(
        owned=dict(required=False, type="bool"),
        configured=dict(required=False, type="bool"),
        mode=dict(required=False, type="str"),
        minor_recoverable_fault=dict(required=False, type="bool"),
        minor_unrecoverable_fault=dict(required=False, type="bool"),
        major_recoverable_fault=dict(required=False, type="bool"),
        major_unrecoverable_fault=dict(required=False, type="bool"),
        keyswitch=dict(required=False, type="str"),
        transitioning=dict(required=False, type="bool"),
        debug=dict(required=False, type="bool"),
    )

    subopts = dict(
        vendor_id=dict(required=False, type="int"),
        device_type=dict(requied=False, type="int"),
        product_code=dict(requied=False, type="int"),
        revision=dict(requied=False, type="str"),
        status=dict(requied=False, type="dict", options=statusopt),
        serial_number=dict(requied=False, type="str"),
        product_name=dict(requied=False, type="str"),
    )

    argspec = dict(cip_identity=dict(type="dict", options=subopts))

    module = AnsibleModule(argument_spec=argspec)

    module = AnsibleModule(argument_spec=argspec)

    logix_util = LogixUtil(module)

    cip_identity_results = []

    if not module.params["cip_identity"]:
        module.fail_json(msg="No CIP identity properties provided.")

    if module.params["cip_identity"]["vendor_id"]:
        if (
            logix_util.plc.info["vendor"]
            == logix_util.cip.VENDORS[module.params["cip_identity"]["vendor_id"]]
        ):
            cip_identity_results.append("vendor_id")
        else:
            module.fail_json(
                msg="Vendor id %s does not match the vendor id %s from this PLC."
                % (
                    module.params["cip_identity"]["vendor_id"],
                    logix_util.cip.VENDORS.get(
                        logix_util.plc.info["vendor"], "UNKNOWN"
                    ),
                )
            )

    if module.params["cip_identity"]["device_type"]:
        if (
            logix_util.plc.info["product_type"]
            == logix_util.cip.PRODUCT_TYPES[
                module.params["cip_identity"]["device_type"]
            ]
        ):
            cip_identity_results.append("device_type")
        else:
            module.fail_json(
                msg="Device type %s does not match the device type %s from this PLC."
                % (
                    module.params["cip_identity"]["device_type"],
                    logix_util.cip.PRODUCT_TYPES.get(
                        logix_util.plc.info["product_type"], "UNKNOWN"
                    ),
                )
            )

    if module.params["cip_identity"]["product_code"]:
        if (
            logix_util.plc.info["product_code"]
            == module.params["cip_identity"]["product_code"]
        ):
            cip_identity_results.append("product_code")
        else:
            module.fail_json(
                msg="Product code %s does not match the product code %s from this PLC."
                % (
                    module.params["cip_identity"]["product_code"],
                    logix_util.plc.info["product_code"],
                )
            )

    if module.params["cip_identity"]["revision"]:
        dot_index = module.params["cip_identity"]["revision"].index(".")
        major_slice = module.params["cip_identity"]["revision"][:dot_index]
        minor_slice = module.params["cip_identity"]["revision"][dot_index + 1:]

        if logix_util.plc.info["revision"]["major"] == int(
            major_slice
        ) and logix_util.plc.info["revision"]["minor"] == int(minor_slice):
            cip_identity_results.append("revision")
        else:
            module.fail_json(
                msg="Revision %s does not match the revision %s from this PLC."
                % (
                    module.params["cip_identity"]["revision"],
                    (
                        "%s.%s"
                        % (
                            logix_util.plc.info["revision"]["major"],
                            str(logix_util.plc.info["revision"]["minor"]).zfill(3),
                        )
                    ),
                )
            )

    if module.params["cip_identity"]["status"]:
        binary_status = logix_util.parse_status_to_binary(logix_util.plc.info["status"])
        status = logix_util.parse_status_to_text(binary_status)

        for value in module.params["cip_identity"]["status"]:
            if module.params["cip_identity"]["status"][value] == "False":
                module.params["cip_identity"]["status"][value] = False
            elif module.params["cip_identity"]["status"][value] == "True":
                module.params["cip_identity"]["status"][value] = True

        for status_key in module.params["cip_identity"]["status"]:
            if module.params["cip_identity"]["status"][status_key]:
                if (
                    status[status_key]
                    == module.params["cip_identity"]["status"][status_key]
                ):
                    cip_identity_results.append("status-%s" % status_key)
                else:
                    module.fail_json(
                        msg="Status %s with the value of %s does not match the Status %s with the value %s from this PLC."
                        % (
                            status_key,
                            module.params["cip_identity"]["status"][status_key],
                            status_key,
                            status[status_key],
                        )
                    )

    if module.params["cip_identity"]["serial_number"]:
        if (
            logix_util.plc.info["serial"]
            == module.params["cip_identity"]["serial_number"]
        ):
            cip_identity_results.append("serial_number")
        else:
            module.fail_json(
                msg="Serial number %s does not match the serial number %s from this PLC."
                % (
                    module.params["cip_identity"]["serial_number"],
                    logix_util.plc.info["serial"],
                )
            )

    if module.params["cip_identity"]["product_name"]:
        if (
            logix_util.plc.info["product_name"]
            == module.params["cip_identity"]["product_name"]
        ):
            cip_identity_results.append("product_name")
        else:
            module.fail_json(
                msg="Product name %s does not match the product name %s from this PLC."
                % (
                    module.params["cip_identity"]["product_name"],
                    logix_util.plc.info["product_name"],
                )
            )

    module.exit_json(
        ansible_module_results="Verified %s properties match the data from this PLC."
        % (", ".join(cip_identity_results)),
        msg="Identity verified correctly.",
    )


if __name__ == "__main__":
    main()
