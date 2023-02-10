import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('nfs-server')

@pytest.fixture()
def role_vars(host):
    if host.system_info.distribution in ['centos', 'redhat']:
        ansible_vars = host.ansible('include_vars', './vars/RedHat.yml')
    else:
        ansible_vars = host.ansible('include_vars', './vars/Debian.yml')
    return ansible_vars['ansible_facts']

def test_service(host, role_vars):
    svc = host.service(role_vars['nfs_service_name'])
    assert svc.is_running
    assert svc.is_enabled
