Backupninja
=========

The intended use of this role is the installation backupninja and do a backup test based in La Brecha Digital needs.

Requirements
------------

* Debian based hosts

Role Variables
--------------
* `ninja`: Dictionary with the options of the role
  * `email_to_report`: Email to send status of the logs
  * `backup_retention_period`: Period of retention of backups (Default: `60D`)
  * `backup_method`: Select the backup method to use (Default: `rdiff`)
  * `include`: List of directories to be included in the backup
  * `exclude`: List of directories to be excluded from the backup
  * `temp_backup_dir`: The directory where the temporal files for the backup
    are going to be stored
  * `backup_dir`: The directory where the backup is going to be stored
  * `execute_hourly`: Set to `True` if you want to run `backupninja` hourly
    (Default: `False`)

Dependencies
------------

None.

Example Playbook
----------------

```yaml
---
- hosts: all
  roles:
    - backupninja
```

License
-------

GPLv2

Author Information
------------------

Lyz (lyz at riseup net)
