Netbox Sync
---

This plugin is a sync plugin for network devices and netbox.

Installation
----

* Install NetBox as per NetBox documentation
* Add to local_requirements.txt:
  * `netbox-sync`
* Install requirements: `./venv/bin/pip install -r local_requirements.txt`
* Add to PLUGINS in NetBox configuration:
  * `'netbox_sync',`
* Run migration: `./venv/bin/python netbox/manage.py migrate`
* Run collectstatic: `./venv/bin/python netbox/manage.py collectstatic --no-input`

