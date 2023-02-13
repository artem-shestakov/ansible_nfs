# NFS

Ansible role to install and setup NFS server

## Requirements

* `community.general`
* `ansible.posix`

## Role Variables

`nfs_client` - describe role of host. `false` if host is NFS server and `true` if host is client and need mount shared directoies. Default: `false`
`nfs_exports` - list of entry for an exported file system. Format of entry is `directory_to_share    client(share_option1,...,share_optionN)`. Default: `[]` 
Example:
```yaml
nfs_exports:
  - /home 192.168.1.0/24(rw,sync,no_root_squash,no_all_squash)
  - /var/backups 192.168.2.1(ro,async,no_subtree_check)
```
`nfs_mount_points` - list of mount points on the NFS client system. Format of entry is `server:shared_directory mount_point_directory` Default: `[]` 
Example:
```yaml
nfs_mount_points:
  - 192.168.1.1:/home /mnt/exports/home
  - 192.168.1.1:/var/backups /mnt/exports/backups
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
