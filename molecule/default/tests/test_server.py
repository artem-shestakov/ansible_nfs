import os
import pytest
import testinfra
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('nfs-server')

# Get role variables from vars
@pytest.fixture()
def role_vars(host):
    if host.system_info.distribution in ['centos', 'redhat']:
        ansible_vars = host.ansible('include_vars', './vars/RedHat.yml')
    else:
        ansible_vars = host.ansible('include_vars', './vars/Debian.yml')
    return ansible_vars['ansible_facts']

# Get server vars
@pytest.fixture()
def server_vars(host):
    ansible_vars = host.ansible('include_vars', f'./molecule/default/host_vars/nfs-server.yml')
    return ansible_vars['ansible_facts']

# Get client vars
@pytest.fixture()
def client_vars(host):
    ansible_vars = host.ansible('include_vars', f'./molecule/default/host_vars/nfs-client.yml')
    return ansible_vars['ansible_facts']

# Check that NFS server is running
def test_service(host, role_vars):
    svc = host.service(role_vars['nfs_service_name'])
    assert svc.is_running
    assert svc.is_enabled

# Check exported directories
def test_exports(host, server_vars):
    if host.system_info.distribution in ['centos', 'redhat']:
        exports = server_vars['nfs_exports_redhat']
    else:
        exports = server_vars['nfs_exports_debian']
    for export in exports:
        assert host.file(export.split(' ')[0]).exists
        assert host.file(export.split(' ')[0]).is_directory
        assert host.file(export.split(' ')[0]).mode == 0o777

# Check sync between server and client
def test_client(host, server_vars, client_vars):
    # Get client host
    host_client=testinfra.get_host(
        f"ansible://nfs-client?ansible_inventory={os.environ['MOLECULE_INVENTORY_FILE']}")
    
    # Create file in export directories
    if host.system_info.distribution in ['centos', 'redhat']:
        exports = server_vars['nfs_exports_redhat']
    else:
        exports = server_vars['nfs_exports_debian']
    for export in exports:
        host.run(f"echo 'test_exports' > {export.split(' ')[-1]}/test_file.txt")

    # Check file and content on client server
    if host.system_info.distribution in ['centos', 'redhat']:
        exports = client_vars['nfs_mount_points_redhat']
    else:
        exports = client_vars['nfs_mount_points_debian']
    for export in exports:
        assert host_client.ansible.get_variables()['inventory_hostname'] == 'nfs-client'
        assert host_client.file(f"{export.split(' ')[-1]}/test_file.txt").exists
        cmd = host_client.run(f"cat {export.split(' ')[-1]}/test_file.txt")
        assert 'test_exports' in cmd.stdout
