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

@pytest.fixture()
def host_vars(host):
    ansible_vars = host.ansible('include_vars', f'./molecule/default/host_vars/nfs-server.yml')
    return ansible_vars['ansible_facts']

def test_service(host, role_vars):
    svc = host.service(role_vars['nfs_service_name'])
    assert svc.is_running
    assert svc.is_enabled

def test_exports(host, host_vars):
    if host.system_info.distribution in ['centos', 'redhat']:
        exports = host_vars['nfs_exports_redhat']
    else:
        exports = host_vars['nfs_exports_debian']
    for export in exports:
        assert host.file(export.split(' ')[0]).exists
        assert host.file(export.split(' ')[0]).is_directory
        host.run(f"echo 'test_exports' > {export.split(' ')[0]}/test_file.txt")