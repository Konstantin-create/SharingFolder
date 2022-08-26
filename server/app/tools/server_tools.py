from __future__ import annotations

import json
import hashlib


def parse_package(package: str) -> dict | None:
    """Function find package type and call functions"""

    try:
        return json.loads(package)
    except:
        return None


def generate_key(client_data: dict):
    """Function to generate """

    return hashlib.sha256(str(client_data).encode()).hexdigest()
