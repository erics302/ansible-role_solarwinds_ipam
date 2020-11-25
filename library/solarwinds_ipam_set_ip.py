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
module: solarwinds_ipam_set_ip

short_description: Record an IPv4 address as in use in Solarwinds IPAM

version_added: "2.7"

description:
    - "Using the solarwinds API, set an IP node record to in use status and add a hostname entry (or remove).  Also disables the solarwinds scanning function for the IP by default."

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
    ipam_ip_address:
        description:
            - IPv4 address to be marked as in use.
        required: true
    ipam_ip_hostname:
        description:
            - String value for the IPAM hostname field.  
        required: false
    state:
        description:
            - present (default) to set the ip as in use and add hostname and scanning setting.
            - absent to set ip as available and remove hostname and return scanning to true.
        

extends_documentation_fragment:

author:
    - Eric Spencer (eric@spencernet.net)
'''
EXAMPLES = '''
    solarwinds_ipam_set_ip:
        ipam_server_addr: "solarwindsserver.example.com:8443"
        ipam_username: "FOO"
        ipam_password: "BAR"
        certcheck: false
        ipam_ip_hostname: "test.example.com"
        ipam_ip_address: "1.0.0.2"
        state: "present"

    solarwinds_ipam_set_ip:
        ipam_server_addr: "solarwindsserver.example.com"
        ipam_username: "FOO"
        ipam_password: "BAR"
        certcheck: false
        ipam_ip_address: "1.0.0.2"
        state: "absent"
    
'''

RETURN = '''
changed:
    description: true is update to IPAM was successful.  false on module failed.
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import json

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        ipam_server_addr=dict(required=True),
        certcheck=dict(type='bool', default=True),
        ipam_username=dict(required=True),
        ipam_password=dict(no_log=True, required=True),
        ipam_ip_address=dict(required=True),
        ipam_ip_hostname=dict(required=False),
        state=dict(default='present'),
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    #Step 1, get the sw ipam ipnodeid for our IP address
    node_id_uri = '/SolarWinds/InformationService/v3/Json/Query?query=SELECT%20uri%20from%20IPAM.IPNode%20where%20IPAddress%20=%20%27'
    url = 'https://' + module.params['ipam_server_addr'] + node_id_uri + module.params['ipam_ip_address'] + '%27'
    resp_node_id = requests.get(url, auth=( module.params['ipam_username'] , module.params['ipam_password'] ), verify=module.params['certcheck'])
    print(resp_node_id.status_code)
    if resp_node_id.status_code != 200:
        result['http_status_code'] = resp_node_id.status_code
        module.fail_json(msg='Failed to connect to IPAM server', **result)
    resp_node_id_json = json.loads(resp_node_id.text)
    if is_empty(resp_node_id_json['results']):
        module.fail_json(msg='Module fail - Provided IP not configured in IPAM', **result)

    #Step 2, Set the values needed to configure SW ipam for the provided IP.
    node_id_uri = '/SolarWinds/InformationService/v3/Json/'
    url = 'https://' + module.params['ipam_server_addr'] + node_id_uri + resp_node_id_json['results'][0]['uri']
    print(url)
    if module.params['state'] == "absent":
        ipam_payload = {"DNSBackward":"","Status":"Available", "SkipScan":"False"}
    else:
        ipam_payload = {"DNSBackward":module.params['ipam_ip_hostname'],"Status":"Reserved", "SkipScan":"True"}

    #Step 3, Deliver the payload to add or remove IPAM details to an IP.
    resp_ip_node_id_query = requests.post(url, auth=( module.params['ipam_username'] , module.params['ipam_password'] ), verify=module.params['certcheck'], json=ipam_payload)
    if resp_ip_node_id_query.status_code != 200:
        result['http_status_code'] = resp_ip_node_id_query.status_code
        module.fail_json(msg='Failed to connect to IPAM server', **result)
    else:
        result['changed'] = True
    print(resp_ip_node_id_query)
    module.exit_json(**result)

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def main():
    run_module()

if __name__ == '__main__':
    main()
