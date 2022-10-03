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
module: ensure_firmware_revision
short_description: Ensure firmware is a specific revision or fail
description:
    - Ensure firmware is a specific revision or fail
author:
- Adam Miller (@maxamillion)
options:
  revision:
    description:
      - firmware revision to validate in the form XX.YYY or XX
    required: false
    type: int
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
from ansible.module_utils._text import to_native, to_text
from ansible_collections.industrial.logix.plugins.module_utils.logix import LogixUtil


def main():

    argspec = dict(
        revision=dict(required=True, type="str"),
    )

    module = AnsibleModule(
        argument_spec=argspec,
    )

    logix_util = LogixUtil(module)

    plc_revision = logix_util.plc.get_plc_info()["revision"]

    # The best I can tell, all ControlLogix controllers revisions are composed
    # of a two digit number signifying the "Major" revision, followed by a dot,
    # followed by a three digit number signifying the "Minor" revision: XX.YYY.
    # Larger major numbers correspond to newer major revisions (typically one
    # major release per year but there are exceptions). Minor releases are less
    # reliable in that regard. For example minor revisions > 500 are
    # redundancy specific and < 500 are non-redundancy
    #
    # In most but not all cases, the major revision is the one people care
    # about and often times a controller revision discussed by only referring
    # the major revision. IE: "That controller is running revision 33", which
    # is why I've put effort into allowing the revision to be specified in that
    #  way
    #
    # MicroLogix or motor controllers or stratix may to be different but let's
    # cross that bridge when we get there.
    # - AN

    # Dictionary to hold major and minor revisions, will eventually be in the
    # form of { 'major': 00, 'minor': 00 }
    revision_param = {}

    ####################
    # Argument Parsing #
    ####################
    # Parse the revision information given to us. If it contains a period, that
    # implies it is in the major.minor form
    if "." in module.params["revision"]:

        # Fail if more than a single decimal is provided
        if module.params["revision"].count(".") > 1:
            module.fail_json(
                msg=(
                    "Controller revision not specified properly. ",
                    "Tried to parse revision `%s` in form Major.Minor,",
                    "but more then one decimal was provided"
                )
                % (module.params["revision"])
            )

        # Determine the index of said period, and slice the revision string
        dot_index = module.params["revision"].index(".")
        major_slice = module.params["revision"][:dot_index]
        minor_slice = module.params["revision"][dot_index + 1:]

        # Attempt to convert major and minor slices. Ask for forgiveness if it
        # fails
        try:
            revision_param["major"] = int(major_slice)
        except ValueError:
            # TODO How to properly fail with invalid parameters?
            module.fail_json(
                msg=(
                    "Controller revision not specified properly. ",
                    "Tried to parse revision `%s` in form Major.Minor, ",
                    "but could not parse major revision `%s` as an integer"
                )
                % (module.params["revision"], major_slice)
            )

        try:
            revision_param["minor"] = int(minor_slice)
        except ValueError:
            module.fail_json(
                msg=(
                    "Controller revision not specified properly. ",
                    "Tried to parse revision `%s` in form Major.Minor, ",
                    "but could not parse minor revision `%s` as an integer"
                )
                % (module.params["revision"], minor_slice)
            )
    else:
        # If no period is found in the revision string, this implies that the
        # string an integer representing the major revision
        try:
            revision_param["major"] = int(module.params["revision"])
        except ValueError:
            module.fail_json(
                msg=(
                    "Controller revision not specified properly. ",
                    "Tried to parse revision `%s` in form `Major`, ",
                    "but could not parse major revision %s as an integer"
                )
                % (module.params["revision"], module.params["revision"])
            )

    #####################
    # Revision Checking #
    #####################

    # check major revision
    if plc_revision["major"] != revision_param["major"]:
        module.fail_json(
            msg=(
                "Major revision %s not confirmed. ",
                "Major revision %s found instead."
            )
            % (revision_param["major"], plc_revision["major"])
        )

    # Check if minor revision was specified
    if "minor" in revision_param:
        # Check minor revision
        if plc_revision["minor"] != revision_param["minor"]:
            module.fail_json(
                msg=(
                    "Major revision %s confirmed but minor revision %s not ",
                    "confirmed. Minor revision %s found instead."
                )
                % (
                    revision_param["major"],
                    revision_param["minor"],
                    plc_revision["minor"],
                )
            )

    # Exit successfully. Check if for minor again to have a specific exit
    # message for each case
    if "minor" in revision_param:
        module.exit_json(
            msg="Revision %s.%s confirmed."
            % (revision_param["major"], revision_param["minor"]),
            changed=False,
        )
    else:
        module.exit_json(
            msg="Revision %s.%s matches major revision %s."
            % (
                plc_revision["major"],
                plc_revision["minor"],
                revision_param["major"]
            ),
            changed=False,
        )


if __name__ == "__main__":
    main()
