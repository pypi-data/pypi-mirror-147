import json
import os
import sys

from ferris_cli.v2 import ApplicationConfigurator
from ferris_cli.v2.services.config import Consul
from .base import PackageState, PackageStateLocal, Secrets, SecretsLocal, Package


is_local_env = os.environ.get('EF_ENV') == 'local'


if is_local_env:
    config_file_name = 'ef_env.json'

    if not os.path.isfile(config_file_name):
        with open(config_file_name, 'w') as sf:
            json.dump({
                "params": {
                    "package_name": "local_package",
                    "package_id": "1234456778"
                },
                "config": {},
                "secrets": {}
            }, sf)

    f = open(config_file_name)
    env_file = json.load(f)

    params = env_file.get('params', {})
    package = Package(
        name=params.get("package_name", "local_package"),
        id=params.get("package_id", "01234567")
    )
    config = env_file.get('config', {})
    secrets = SecretsLocal(env_file.get('secrets', {}))

else:
    params = json.loads(sys.argv[1]) or {}

    package = Package(
        name=params.get("package_name"),
        id=params.get("package_id")
    )

    config = ApplicationConfigurator.get(package.name) or {}
    secrets = Secrets(params.pop("secrets", {}), config, package)
    _env = os.environ.items()


state = PackageState(package, config) if not is_local_env else PackageStateLocal(package, config)

