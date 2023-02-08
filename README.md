# NFS

Ansible role to install and setup NFS server

## Requirements

* `community.general`
* `ansible.posix`

## Role Variables

`nfs_exports` - list of entry for an exported file system. Format of entry is `directory_to_share    client(share_option1,...,share_optionN)`. Default: `[]` 
Example:
```yaml
nfs_exports:
  - /home 192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)
  - /var/backups 192.168.2.1(ro,async,no_subtree_check)
```

## Example Playbook

```yaml
to do
```
## License

BSD

## Author Information

Artem Shestakov  
E-mail: artem.s.shestakov@gmail.com
