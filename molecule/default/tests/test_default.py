import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package", [
    ("backupninja"),
    ("hwinfo"),
    ("debconf-utils"),
    ("flashrom"),
    ("rdiff-backup"),
    ("postfix"),
])
def test_required_packages_are_installed(host, package):
    assert host.package(package).is_installed


@pytest.mark.parametrize("directories", [
    ("/backups"),
    ("/var/backups"),
])
def test_required_directories_exist(host, directories):
    file = host.file(directories)
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0755'


def test_ninja_global_config(host):
    file = host.file('/etc/backupninja.conf')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0600'
    assert file.contains('reportemail = lyz@gentooza.me')
    assert file.contains('when = everyday at 13')


def test_ninja_sys_backup_config(host):
    file = host.file('/etc/backup.d/10.sys')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0600'


@pytest.mark.parametrize("sys_files", [
    ("/var/backups/debconfsel.txt"),
    ("/var/backups/dpkg-selections.txt"),
    ("/var/backups/hardware.txt"),
    ("/var/backups/sysreport.txt"),
])
def test_ninja_sys_files_were_created_(host, sys_files):
    file = host.file(sys_files)
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0600'


def test_ninja_rdiff_backup_config(host):
    file = host.file('/etc/backup.d/20.rdiff')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0600'
    assert file.contains('nicelevel = 19')
    assert file.contains('label = backupninja_debian_stretch')
    assert file.contains('type = local')
    assert file.contains('keep = 60D')
    assert file.contains("include = /var/spool/cron/crontabs")
    assert file.contains("include = /var/backups")
    assert file.contains("include = /etc")
    assert file.contains("include = /root")
    assert file.contains("include = /home")
    assert file.contains("include = /usr/local/bin")
    assert file.contains("include = /usr/local/sbin")
    assert file.contains("include = /var/lib/dpkg/status")
    assert file.contains("include = /var/lib/dpkg/status-old")
    assert file.contains("exclude = /tmp")
    assert file.contains("directory = /backups")


def test_ninja_rdiff_worked(host):
    file = host.file('/backups/backupninja_debian_stretch')
    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0755'
