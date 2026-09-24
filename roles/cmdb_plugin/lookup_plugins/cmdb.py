from __future__ import annotations

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
import json
import os
from typing import Any, List


class LookupModule(LookupBase):
    """Simple CMDB lookup plugin.

    Usage examples in a playbook:
      - name: load all cmdb entries
        set_fact:
          cmdb_all: "{{ lookup('cmdb') }}"

      - name: find host by name
        set_fact:
          host_info: "{{ lookup('cmdb', host='db1') | first }}"

      - name: search by key/value
        set_fact:
          matches: "{{ lookup('cmdb', search_key='role', search_value='db') }}"

    The lookup accepts either a `path` kwarg to a JSON file, or looks
    for `roles/cmdb_plugin/files/cmdb.json` relative to the playbook dir.
    The JSON should be an array of objects (dictionaries) representing
    CMDB entries.
    """

    def run(self, terms: List[Any], variables: dict = None, **kwargs) -> List[Any]:
        variables = variables or {}

        # Accept either terms[0] as a path or kw args: path, host, search_key, search_value
        path = None
        if terms:
            path = terms[0]

        file_path = kwargs.get('path', path)
        host = kwargs.get('host')
        search_key = kwargs.get('search_key')
        search_value = kwargs.get('search_value')

        if not file_path:
            playbook_dir = variables.get('__playbook_dir') or os.getcwd()
            file_path = os.path.join(playbook_dir, 'roles', 'cmdb_plugin', 'files', 'cmdb.json')

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            raise AnsibleError(f'cmdb lookup: failed to read {file_path}: {e}')

        if not isinstance(data, list):
            raise AnsibleError('cmdb lookup: expected JSON array of objects')

        results = []

        if host:
            for item in data:
                if not isinstance(item, dict):
                    continue
                if item.get('hostname') == host or item.get('name') == host:
                    results.append(item)
        elif search_key and search_value is not None:
            for item in data:
                if not isinstance(item, dict):
                    continue
                if str(item.get(search_key)) == str(search_value):
                    results.append(item)
        else:
            results = data

        return results
