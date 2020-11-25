#!/usr/bin/python

# Copyright: (c) 2019, Eric Spencer <eric@spencernet.net
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: solarwinds_ipam_get_next_ip

short_description: solarwinds IPAM.SubnetManagement.getFirstAvailableIp

version_added: "2.7"

description:
    - "Connects to a solarwinds IPAM rest API to find the next available IPv4 address in a subnet.  It doesn't actually update the IPAM database in anyway.  Uses IPAM.SubnetManagement.GetFirstAvailableIp"

options:
    ipam_server_addr:
        description:
            - URL/IP of the solarwinds ipam server.  Include colon and nonstandard port number if applicable.
        required: true
    certcheck:
        description:
            - Check ssl cert validity of Solarwinds IPAM server.
        required: false
        default: true
    ipam_username:
        description:
            - Username for solarwinds api access.
        required: true
    ipam_password:
        description:
            - password for solarwinds api access.
        required: true
    ipam_subnet:
        description:
            - IPv4 subnet address from which you want to find an available IP.
        required: true
    ipam_mask:
        description:
            - CIDR notation mask of the subnet from which you want to find an available IP.
        required: true

        

extends_documentation_fragment:

author:
    - Eric Spencer (eric@spencernet.net)
'''

EXAMPLES = '''
    solarwinds_ipam_get_next_available_ip:
        ipam_subnet: "10.0.0.0"
        ipam_cidr_mask: "24"
        ipam_password: "BAR"
        ipam_username: "FOO"
        certcheck: false
        ipam_server_addr: "solarwindsserver.example.com:8443"
'''

RETURN = '''
changed:
    description: Always false as we aren't actually making any changes, just retrieving a value.  Document the use of return_ip via different module.
    type: str
    returned: always
return_ip:
    description: The next free IPv4 address in the subnet provided via module args OR the string "Not found" when the provided subnet/mask combination is not configured in IPAM or there are no free IP addersses in the provided subnet"
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import re

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        ipam_server_addr=dict(required=True),
        certcheck=dict(type='bool', default=True),
        ipam_username=dict(required=True),
        ipam_password=dict(no_log=True, required=True),
        ipam_subnet=dict(required=True),
        ipam_cidr_mask=dict(required=True),
    )

    result = dict(
        changed=False,
        return_ip=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ipam_uri = '/SolarWinds/InformationService/v3/Json/Invoke/IPAM.SubnetManagement/GetFirstAvailableIp'
    url = 'https://' + module.params['ipam_server_addr'] + ipam_uri
    subnet_dict = {"subnetAddress":module.params['ipam_subnet'],"subnetCidr":module.params['ipam_cidr_mask']}

    resp = requests.post(url, auth=( module.params['ipam_username'] , module.params['ipam_password'] ), verify=module.params['certcheck'], json=subnet_dict)
    if resp.status_code != 200:
        result['http_status_code'] = resp.status_code
        module.fail_json(msg='Failed to connect to IPAM server', **result)

    result['return_ip'] = re.sub('"', '', resp.content)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
