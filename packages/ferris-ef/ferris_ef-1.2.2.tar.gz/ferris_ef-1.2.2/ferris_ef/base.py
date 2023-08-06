import json
import os
import sys
import requests

from ferris_cli.v2 import ApplicationConfigurator
from ferris_cli.v2.services.config import Consul

def get_param(paramname):
    fa = json.loads(sys.argv[1])
    try:
        return fa[paramname]
    except Exception as e:
        print(f"Parameter {paramname} not found!")


def get_secret(secretname):
    fa = json.loads(sys.argv[1])
    try:
        return fa['secrets'][secretname]
    except Exception as e:
        print(f"Secret {secretname} not found!")


class PackageState:

    def __init__(self, package, config):
        self._package = package
        self._package_state_key = f"{self._package.name}.state"
        self.consul = Consul(
            consul_host=config.get('CONSUL_HOST'),
            constul_port=config.get('CONSUL_PORT')
        )

    def get(self):
        index, data = self.consul.client.kv.get(self._package_state_key, index=None)
        return json.loads(data['Value']) if data and 'Value' in data else {}

    def put(self, key, value):
        try:
            state = self.get()
        except Exception as e:
            state = {}

        state[key] = value
        self.consul.put_item(self._package_state_key, json.dumps(state))


class PackageStateLocal:

    def __init__(self, package, config):
        self._package = package
        self._package_state_key = "ef_package_state.json"

        if not os.path.isfile(self._package_state_key):
            with open(self._package_state_key, 'w') as sf:
                json.dump({}, sf)

    def get(self):
        sf = open(self._package_state_key)
        data = json.load(sf)

        return data

    def put(self, key, value):
        state = self.get()
        state[key] = value

        with open(self._package_state_key, 'w') as sf:
            json.dump(state, sf)


class Secrets:

    def __init__(self, secrets, config, package=None):
        self.secrets = secrets
        self.package = package
        self.config = config

    def get(self, name):
        return self.secrets.get(name) or self._get_from_api(name)

    def set(self, name, value, context):
        r = requests.post(
            url=f"{os.environ.get('SECRETS_API_URL')}",
            json=dict(
                name=name,
                value=value,
                context=context,
                package_id=self.package.id or None
            )
        )

        return r.status_code, r.text

    def _get_from_api(self, name):
        r = requests.get(
            url=f"{os.environ.get('SECRETS_API_URL')}by-name",
            params=dict(
                name=name,
                package_id=self.package.id
            )
        ).json()

        return r.get('value') or None


class SecretsLocal:

    def __init__(self, secrets, package=None):
        self.secrets = secrets
        self.package = package

    def get(self, name):
        return self.secrets.get(name, {})


class Package:
    def __init__(self, name, id):
        self.name = name
        self.id = id