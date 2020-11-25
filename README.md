# Ansible Role: ansible-role_solarwinds_ipam

<!-- TOC -->

- [Ansible Role: ansible-role_solarwinds_ipam](#ansible-role-ansible-role_solarwinds_ipam)
    - [ansible-role_solarwinds_ipam - Description](#ansible-role_solarwinds_ipam---description)
    - [ansible-role_solarwinds_ipam - Requirements](#ansible-role_solarwinds_ipam---requirements)
    - [Using the ansible-solarwinds_ipam role within an Ansible Playbook](#using-the-ansible-solarwinds_ipam-role-within-an-ansible-playbook)
        - [Example Ansible Playbook using ansible-role_solarwinds_ipam role](#example-ansible-playbook-using-ansible-role_solarwinds_ipam-role)
    - [Custom Variables](#custom-variables)
    - [Local development testing](#local-development-testing)
        - [Pre-Requisites](#pre-requisites)
    - [Contributing](#contributing)
    - [History](#history)
    - [Credits](#credits)

<!-- /TOC -->

## ansible-role_solarwinds_ipam - Description

The modules can do three things to start:

Get the next available IP from a subnet.
Mark an IP as status=”reserved” and add a hostname text string.
Mark an IP as “available” and set all fields for the record back to default.

## ansible-role_solarwinds_ipam - Requirements

Call these role from your playbook, and the modules within become available to all other roles called from the playbook.

## Using the ansible-solarwinds_ipam role within an Ansible Playbook

### Example Ansible Playbook using ansible-role_solarwinds_ipam role

```bash
---
- hosts: localhost
  gather_facts: no
  roles:
    - ansible-role_solarwinds_ipam

```

## Custom Variables

See library files for modules[`libary`](library/).

## Local development testing

### Pre-Requisites

The following components are required for executing this playbook on local desktop

1. [Ansible 2.7.0+](http://docs.ansible.com/ansible/latest/intro_installation.html)
2. [Git 2.11+](https://git-scm.com/downloads)
3. [Python 2.7+](https://www.python.org/downloads/)
4. [Python Package Index (PIP) 9.0.1+](https://pip.pypa.io/en/stable/installing/)
5. [Molecule 2.7.0](https://molecule.readthedocs.io/en/latest/installation.html)

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md)

## History

See [CHANGELOG](CHANGELOG.md)

## Credits

See [AUTHORS](AUTHORS.md)
