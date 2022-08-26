from __future__ import annotations

import json
import hashlib


def parse_package(package: str) -> dict | None:
    """Function find package type and call functions"""

    json_package = {}

    package = package.splitlines()
    package_type = package[0].split()[0]
    if package_type == 'GET':
        return _get_package(package)
    elif package_type == 'POST':
        return _post_package(package)
    else:
        print('Not supported package')
        return None


def _get_package(package) -> dict:
    """Function to parse server get package"""

    return {
        'method': 'GET',
        'url': package[0].split()[1],
        'http': package[0].split()[2],
        'host': package[1].split()[1],
        'user_agent': package[2].split()[1]
    }


def _post_package(package) -> dict:
    """Function to parse server post package"""

    return {
        'method': 'POST',
        'url': package[0].split()[1],
        'http': package[0].split()[2],
        'host': package[1].split()[1],
        'user_agent': package[2].split()[1],
        'json': json.loads(package[-1])
    }


def generate_key(client_data: dict):
    """Function to generate """

    return hashlib.sha256(str(client_data).encode()).hexdigest()
