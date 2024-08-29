# IN ACTIVE DEVELOPMENT community.cip Collection for Ansible
<!-- Add CI and code coverage badges here. Samples included below. -->
[![CI](https://github.com/ansible-collections/community.cip/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.cip/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.cip)](https://codecov.io/gh/ansible-collections/community.cip)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->

Collection to manage Programmable Logic Controllers (PLC) via the Common Industrial Protocol (CIP). This utilizes the [pycomm3 python library](https://github.com/ottowayi/pycomm3) to communicate and manage devices. While this collection may provide functionality for any CIP device, it has only been tested against Allen Bradley PLCs at this time. This scope of this collection is limited to writing tags and verifying other properties of the PLC device limited to the capabilities of the pycomm3 Python library.

## Development Environment

To use this while developing, run the following commands from within your local directory you pulled to this git repo to in order to symlink this git repo to the appropriate Ansible Collection path

```shell
mkdir -p ~/.ansible/collections/ansible_collections/community
ln -s $(pwd) ~/.ansible/collections/ansible_collections/community/cip
```

## Execution Environment

Execution environments allow for a standardized and containerized environment to run Ansible in. This is used heavily in situations like Ansible Automation Platform. [docs/execution-environment](docs/execution-environment) contains an example execution environment that can be used with the community.cip collection. For more information, refer to the [ansible-builder](https://ansible-builder.readthedocs.io/en/stable/) documentation.

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

<!--List available communication channels. In addition to channels specific to your collection, we also recommend to use the following ones.-->

Join the Ansible forum to ask questions, get help, and interact with us.

- [Get Help](https://forum.ansible.com/c/help/6): get help or help others.
  Please add appropriate tags if you start new discussions; for example,
  use the [`edge`](https://forum.ansible.com/tags/c/help/6/none/edge) tag.
- [Social Spaces](https://forum.ansible.com/c/chat/4): meet and interact with
  fellow enthusiasts.
- [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide
  announcements including social events.

We announce releases and important changes through Ansible's [Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn).

We also take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, fill up and include the CONTRIBUTING.md file containing how and where users can create issues to report problems or request features for this collection. List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/devel/community/index.html). List the current maintainers (contributors with write or higher access to the repository). The following can be included:-->

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](https://docs.ansible.com/ansible/devel/community/contributor_path.html)!

We use the following guidelines:

- [CONTRIBUTING](https://docs.ansible.com/ansible/devel/community/contributor_path.html#making-your-first-contribution)
- [REVIEW_CHECKLIST](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
- [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
- [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](https://docs.ansible.com/ansible/devel/community/maintainers.html).

## Governance

<!--Describe how the collection is governed. Here can be the following text:-->

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->
[Python pycomm3 library](https://github.com/ottowayi/pycomm3)

### Supported connections

<!-- Optional. If your collection supports only specific connection types (such as HTTPAPI, netconf, or others), list them here. -->

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. It can include the following examples of installation and upgrade (change community.cip correspondingly):-->

### Gather CIP Facts

```shell
ansible-playbook playbooks/cip_facts.yml -i docs/example/inventory.ini
```

### Verify CIP Identity

```shell
ansible-playbook playbooks/verify_cip_identity.yml -i docs/example/inventory.ini
```

### Verify Tag Value

```shell
ansible-playbook playbooks/verify_valid_tag_value.yml -i docs/example/inventory.ini
```

### Verify Firmware Version

```shell
ansible-playbook playbooks/verify_firmware_version.yml -i docs/example/inventory.ini
```

### Ensure Tags are what we want them to be

```shell
ansible-playbook playbooks/ensure_tags.yml -i docs/example/inventory.ini
```

### Do all above tasks

```shell
ansible-playbook playbooks/main.yml -i docs/example/inventory.ini
```

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```bash
ansible-galaxy collection install community.cip
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.cip
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install community.cip --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install community.cip:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/community.cip/tree/main/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [News for Maintainers](https://forum.ansible.com/tag/news-for-maintainers)

## Friendly Reminder

PLCs control real world objects that move, spin, and interact with humans. This collection can communicate with PLCs, thus, it can make changes that alter objects in the real world. It is highly recommended to develop and test in a controlled, safe place before atttempting to change or modify any control system running in a production capacity.

## Licensing

[MIT](https://opensource.org/licenses/MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
