#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2015, René Moser <mail@renemoser.net>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: cs_template
short_description: Manages templates on Apache CloudStack based clouds.
description:
  - Register a template from URL, create a template from a ROOT volume of a stopped VM or its snapshot, extract and delete templates.
version_added: '2.0'
author: "René Moser (@resmo)"
options:
  name:
    description:
      - Name of the template.
    required: true
  url:
    description:
      - URL of where the template is hosted on C(state=present).
      - URL to which the template would be extracted on C(state=extracted).
      - Mutually exclusive with C(vm).
  vm:
    description:
      - VM name the template will be created from its volume or alternatively from a snapshot.
      - VM must be in stopped state if created from its volume.
      - Mutually exclusive with C(url).
  snapshot:
    description:
      - Name of the snapshot, created from the VM ROOT volume, the template will be created from.
      - C(vm) is required together with this argument.
  os_type:
    description:
      - OS type that best represents the OS of this template.
  checksum:
    description:
      - The MD5 checksum value of this template.
      - If set, we search by checksum instead of name.
    default: false
  is_ready:
    description:
      - This flag is used for searching existing templates.
      - If set to C(true), it will only list template ready for deployment e.g. successfully downloaded and installed.
      - Recommended to set it to C(false).
    default: false
  is_public:
    description:
      - Register the template to be publicly available to all users.
      - Only used if C(state) is present.
    default: false
  is_featured:
    description:
      - Register the template to be featured.
      - Only used if C(state) is present.
    default: false
  is_dynamically_scalable:
    description:
      - Register the template having XS/VMWare tools installed in order to support dynamic scaling of VM CPU/memory.
      - Only used if C(state) is present.
    default: false
  cross_zones:
    description:
      - Whether the template should be synced or removed across zones.
      - Only used if C(state) is present or absent.
    default: false
  mode:
    description:
      - Mode for the template extraction.
      - Only used if C(state=extracted).
    required: false
    default: http_download
    choices: [ http_download, ftp_upload ]
  domain:
    description:
      - Domain the template, snapshot or VM is related to.
  account:
    description:
      - Account the template, snapshot or VM is related to.
  project:
    description:
      - Name of the project the template to be registered in.
  zone:
    description:
      - Name of the zone you wish the template to be registered or deleted from.
      - If not specified, first found zone will be used.
  template_filter:
    description:
      - Name of the filter used to search for the template.
    required: false
    default: self
    choices: [ featured, self, selfexecutable, sharedexecutable, executable, community ]
  hypervisor:
    description:
      - Name the hypervisor to be used for creating the new template.
      - Relevant when using C(state=present).
    choices: [ KVM, VMware, BareMetal, XenServer, LXC, HyperV, UCS, OVM, Simulator ]
  requires_hvm:
    description:
      - true if this template requires HVM.
    default: false
  password_enabled:
    description:
      - True if the template supports the password reset feature.
    default: false
  template_tag:
    description:
      - the tag for this template.
  sshkey_enabled:
    description:
      - True if the template supports the sshkey upload feature.
    default: false
  is_routing:
    description:
      - True if the template type is routing i.e., if template is used to deploy router.
      - Only considered if C(url) is used.
  format:
    description:
      - The format for the template.
      - Relevant when using C(state=present).
    choices: [ QCOW2, RAW, VHD, OVA ]
  is_extractable:
    description:
      - True if the template or its derivatives are extractable.
    default: false
  details:
    description:
      - Template details in key/value pairs.
  bits:
    description:
      - 32 or 64 bits support.
    required: false
    default: 64
  display_text:
    description:
      - Display text of the template.
  state:
    description:
      - State of the template.
    required: false
    default: present
    choices: [ present, absent, extracted ]
  poll_async:
    description:
      - Poll async jobs until job has finished.
    default: true
  tags:
    description:
      - List of tags. Tags are a list of dictionaries having keys C(key) and C(value).
      - "To delete all tags, set a empty list e.g. C(tags: [])."
    aliases: [ tag ]
    version_added: "2.4"
extends_documentation_fragment: cloudstack
'''

EXAMPLES = '''
- name: register a systemvm template
  local_action:
    module: cs_template
    name: systemvm-vmware-4.5
    url: "http://packages.shapeblue.com/systemvmtemplate/4.5/systemvm64template-4.5-vmware.ova"
    hypervisor: VMware
    format: OVA
    cross_zones: yes
    os_type: Debian GNU/Linux 7(64-bit)

- name: create a template from a stopped virtual machine's volume
  local_action:
    module: cs_template
    name: debian-base-template
    vm: debian-base-vm
    os_type: Debian GNU/Linux 7(64-bit)
    zone: tokio-ix
    password_enabled: yes
    is_public: yes

- name: create a template from a virtual machine's root volume snapshot
  local_action:
    module: cs_template
    name: debian-base-template
    vm: debian-base-vm
    snapshot: ROOT-233_2015061509114
    os_type: Debian GNU/Linux 7(64-bit)
    zone: tokio-ix
    password_enabled: yes
    is_public: yes

- name: Remove a template
  local_action:
    module: cs_template
    name: systemvm-4.2
    cross_zones: yes
    state: absent
'''

RETURN = '''
---
id:
  description: UUID of the template.
  returned: success
  type: string
  sample: a6f7a5fc-43f8-11e5-a151-feff819cdc9f
name:
  description: Name of the template.
  returned: success
  type: string
  sample: Debian 7 64-bit
display_text:
  description: Display text of the template.
  returned: success
  type: string
  sample: Debian 7.7 64-bit minimal 2015-03-19
checksum:
  description: MD5 checksum of the template.
  returned: success
  type: string
  sample: 0b31bccccb048d20b551f70830bb7ad0
status:
  description: Status of the template.
  returned: success
  type: string
  sample: Download Complete
is_ready:
  description: True if the template is ready to be deployed from.
  returned: success
  type: boolean
  sample: true
is_public:
  description: True if the template is public.
  returned: success
  type: boolean
  sample: true
is_featured:
  description: True if the template is featured.
  returned: success
  type: boolean
  sample: true
is_extractable:
  description: True if the template is extractable.
  returned: success
  type: boolean
  sample: true
format:
  description: Format of the template.
  returned: success
  type: string
  sample: OVA
os_type:
  description: Typo of the OS.
  returned: success
  type: string
  sample: CentOS 6.5 (64-bit)
password_enabled:
  description: True if the reset password feature is enabled, false otherwise.
  returned: success
  type: boolean
  sample: false
sshkey_enabled:
  description: true if template is sshkey enabled, false otherwise.
  returned: success
  type: boolean
  sample: false
cross_zones:
  description: true if the template is managed across all zones, false otherwise.
  returned: success
  type: boolean
  sample: false
template_type:
  description: Type of the template.
  returned: success
  type: string
  sample: USER
created:
  description: Date of registering.
  returned: success
  type: string
  sample: 2015-03-29T14:57:06+0200
template_tag:
  description: Template tag related to this template.
  returned: success
  type: string
  sample: special
hypervisor:
  description: Hypervisor related to this template.
  returned: success
  type: string
  sample: VMware
mode:
  description: Mode of extraction
  returned: success
  type: string
  sample: http_download
state:
  description: State of the extracted template
  returned: success
  type: string
  sample: DOWNLOAD_URL_CREATED
url:
  description: Url to which the template is extracted to
  returned: success
  type: string
  sample: "http://1.2.3.4/userdata/eb307f13-4aca-45e8-b157-a414a14e6b04.ova"
tags:
  description: List of resource tags associated with the template.
  returned: success
  type: dict
  sample: '[ { "key": "foo", "value": "bar" } ]'
zone:
  description: Name of zone the template is registered in.
  returned: success
  type: string
  sample: zuerich
domain:
  description: Domain the template is related to.
  returned: success
  type: string
  sample: example domain
account:
  description: Account the template is related to.
  returned: success
  type: string
  sample: example account
project:
  description: Name of project the template is related to.
  returned: success
  type: string
  sample: Production
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.cloudstack import (
    AnsibleCloudStack,
    cs_argument_spec,
    cs_required_together,
    CS_HYPERVISORS
)


class AnsibleCloudStackTemplate(AnsibleCloudStack):

    def __init__(self, module):
        super(AnsibleCloudStackTemplate, self).__init__(module)
        self.returns = {
            'checksum': 'checksum',
            'status': 'status',
            'isready': 'is_ready',
            'templatetag': 'template_tag',
            'sshkeyenabled': 'sshkey_enabled',
            'passwordenabled': 'password_enabled',
            'tempaltetype': 'template_type',
            'ostypename': 'os_type',
            'crossZones': 'cross_zones',
            'isextractable': 'is_extractable',
            'isfeatured': 'is_featured',
            'ispublic': 'is_public',
            'format': 'format',
            'hypervisor': 'hypervisor',
            'url': 'url',
            'extractMode': 'mode',
            'state': 'state',
        }

    def _get_args(self):
        args = {
            'name': self.module.params.get('name'),
            'displaytext': self.get_or_fallback('display_text', 'name'),
            'bits': self.module.params.get('bits'),
            'isdynamicallyscalable': self.module.params.get('is_dynamically_scalable'),
            'isextractable': self.module.params.get('is_extractable'),
            'isfeatured': self.module.params.get('is_featured'),
            'ispublic': self.module.params.get('is_public'),
            'passwordenabled': self.module.params.get('password_enabled'),
            'requireshvm': self.module.params.get('requires_hvm'),
            'templatetag': self.module.params.get('template_tag'),
            'ostypeid': self.get_os_type(key='id'),
        }

        if not args['ostypeid']:
            self.module.fail_json(msg="Missing required arguments: os_type")

        return args

    def get_root_volume(self, key=None):
        args = {
            'account': self.get_account(key='name'),
            'domainid': self.get_domain(key='id'),
            'projectid': self.get_project(key='id'),
            'virtualmachineid': self.get_vm(key='id'),
            'type': "ROOT"
        }
        volumes = self.query_api('listVolumes', **args)
        if volumes:
            return self._get_by_key(key, volumes['volume'][0])
        self.module.fail_json(msg="Root volume for '%s' not found" % self.get_vm('name'))

    def get_snapshot(self, key=None):
        snapshot = self.module.params.get('snapshot')
        if not snapshot:
            return None

        args = {
            'account': self.get_account(key='name'),
            'domainid': self.get_domain(key='id'),
            'projectid': self.get_project(key='id'),
            'volumeid': self.get_root_volume('id')
        }
        snapshots = self.query_api('listSnapshots', **args)
        if snapshots:
            for s in snapshots['snapshot']:
                if snapshot in [s['name'], s['id']]:
                    return self._get_by_key(key, s)
        self.module.fail_json(msg="Snapshot '%s' not found" % snapshot)

    def create_template(self):
        template = self.get_template()
        if not template:
            self.result['changed'] = True

            args = self._get_args()
            snapshot_id = self.get_snapshot(key='id')
            if snapshot_id:
                args['snapshotid'] = snapshot_id
            else:
                args['volumeid'] = self.get_root_volume('id')

            if not self.module.check_mode:
                template = self.query_api('createTemplate', **args)

                poll_async = self.module.params.get('poll_async')
                if poll_async:
                    template = self.poll_job(template, 'template')
        if template:
            template = self.ensure_tags(resource=template, resource_type='Template')

        return template

    def register_template(self):
        required_params = [
            'format',
            'url',
            'hypervisor',
        ]
        self.module.fail_on_missing_params(required_params=required_params)
        template = self.get_template()
        if not template:
            self.result['changed'] = True
            args = self._get_args()
            args.update({
                'url': self.module.params.get('url'),
                'format': self.module.params.get('format'),
                'checksum': self.module.params.get('checksum'),
                'isextractable': self.module.params.get('is_extractable'),
                'isrouting': self.module.params.get('is_routing'),
                'sshkeyenabled': self.module.params.get('sshkey_enabled'),
                'hypervisor': self.get_hypervisor(),
                'domainid': self.get_domain(key='id'),
                'account': self.get_account(key='name'),
                'projectid': self.get_project(key='id'),
            })

            if not self.module.params.get('cross_zones'):
                args['zoneid'] = self.get_zone(key='id')
            else:
                args['zoneid'] = -1

            if not self.module.check_mode:
                res = self.query_api('registerTemplate', **args)
                template = res['template']
        return template

    def get_template(self):
        args = {
            'isready': self.module.params.get('is_ready'),
            'templatefilter': self.module.params.get('template_filter'),
            'domainid': self.get_domain(key='id'),
            'account': self.get_account(key='name'),
            'projectid': self.get_project(key='id')
        }
        if not self.module.params.get('cross_zones'):
            args['zoneid'] = self.get_zone(key='id')

        # if checksum is set, we only look on that.
        checksum = self.module.params.get('checksum')
        if not checksum:
            args['name'] = self.module.params.get('name')

        templates = self.query_api('listTemplates', **args)
        if templates:
            # if checksum is set, we only look on that.
            if not checksum:
                return templates['template'][0]
            else:
                for i in templates['template']:
                    if 'checksum' in i and i['checksum'] == checksum:
                        return i
        return None

    def extract_template(self):
        template = self.get_template()
        if not template:
            self.module.fail_json(msg="Failed: template not found")

        args = {
            'id': template['id'],
            'url': self.module.params.get('url'),
            'mode': self.module.params.get('mode'),
            'zoneid': self.get_zone(key='id')
        }
        self.result['changed'] = True

        if not self.module.check_mode:
            template = self.query_api('extractTemplate', **args)

            poll_async = self.module.params.get('poll_async')
            if poll_async:
                template = self.poll_job(template, 'template')
        return template

    def remove_template(self):
        template = self.get_template()
        if template:
            self.result['changed'] = True

            args = {
                'id': template['id']
            }
            if not self.module.params.get('cross_zones'):
                args['zoneid'] = self.get_zone(key='id')

            if not self.module.check_mode:
                res = self.query_api('deleteTemplate', **args)

                poll_async = self.module.params.get('poll_async')
                if poll_async:
                    res = self.poll_job(res, 'template')
        return template


def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(
        name=dict(required=True),
        display_text=dict(),
        url=dict(),
        vm=dict(),
        snapshot=dict(),
        os_type=dict(),
        is_ready=dict(type='bool', default=False),
        is_public=dict(type='bool', default=True),
        is_featured=dict(type='bool', default=False),
        is_dynamically_scalable=dict(type='bool', default=False),
        is_extractable=dict(type='bool', default=False),
        is_routing=dict(type='bool'),
        checksum=dict(),
        template_filter=dict(default='self', choices=['featured', 'self', 'selfexecutable', 'sharedexecutable', 'executable', 'community']),
        hypervisor=dict(choices=CS_HYPERVISORS),
        requires_hvm=dict(type='bool', default=False),
        password_enabled=dict(type='bool', default=False),
        template_tag=dict(),
        sshkey_enabled=dict(type='bool', default=False),
        format=dict(choices=['QCOW2', 'RAW', 'VHD', 'OVA'], ),
        details=dict(),
        bits=dict(type='int', choices=[32, 64], default=64),
        state=dict(choices=['present', 'absent', 'extracted'], default='present'),
        cross_zones=dict(type='bool', default=False),
        mode=dict(choices=['http_download', 'ftp_upload'], default='http_download'),
        zone=dict(),
        domain=dict(),
        account=dict(),
        project=dict(),
        poll_async=dict(type='bool', default=True),
        tags=dict(type='list', aliases=['tag']),
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_together=cs_required_together(),
        mutually_exclusive=(
            ['url', 'vm'],
            ['zone', 'cross_zones'],
        ),
        supports_check_mode=True
    )

    acs_tpl = AnsibleCloudStackTemplate(module)

    state = module.params.get('state')
    if state in ['absent']:
        tpl = acs_tpl.remove_template()

    elif state in ['extracted']:
        tpl = acs_tpl.extract_template()

    else:
        if module.params.get('url'):
            tpl = acs_tpl.register_template()
        elif module.params.get('vm'):
            tpl = acs_tpl.create_template()
        else:
            module.fail_json(msg="one of the following is required on state=present: url,vm")

    result = acs_tpl.get_result(tpl)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
