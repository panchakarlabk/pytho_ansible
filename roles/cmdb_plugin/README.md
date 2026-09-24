# CMDB Plugin role (example)

This role demonstrates a tiny Ansible lookup plugin for a simplified CMDB stored as JSON.

Files added:
- `lookup_plugins/cmdb.py` — Ansible lookup plugin that reads a JSON array of objects.
- `files/cmdb.json` — Sample CMDB data used by the plugin.
- `defaults/main.yml` — Default variables.

Usage examples (in a playbook):

Load all entries:

  - name: Load CMDB
    set_fact:
      cmdb_all: "{{ lookup('cmdb') }}"

Find a host by name or hostname:

  - name: Get host info
    set_fact:
      host_info: "{{ lookup('cmdb', host='db1') | first }}"

Search by key/value:

  - name: Find db role hosts
    set_fact:
      db_hosts: "{{ lookup('cmdb', search_key='role', search_value='db') }}"

Custom path to CMDB JSON:

  - name: Use external CMDB file
    set_fact:
      cmdb_external: "{{ lookup('cmdb', path='/etc/cmdb/cmdb.json') }}"

Notes:
- This is an example scaffold. For production, replace the JSON file with a real backend
  (REST API, database, NetBox, ServiceNow) and extend the plugin to support create/update/delete,
  authentication, caching, and error handling as needed.
