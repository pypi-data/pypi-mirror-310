def now():
    from datetime import datetime

    return datetime.utcnow()


def uuid_parts() -> (str, str):
    import uuid
    import time

    timestamp = int(time.time() * 100_000)
    random_part = uuid.uuid4().hex[:8]

    return (timestamp, random_part)


def uuid() -> str:
    timestamp, random_part = uuid_parts()

    return f"{timestamp}-{random_part}"


def uuid_to_parts(uuid: str) -> (str, str):
    timestamp, random_part = uuid.split("-")

    return (timestamp, random_part)


def get_dkdc_dir() -> str:
    import os

    dirpath = os.path.join(os.path.expanduser("~"), ".dkdc")

    os.makedirs(dirpath, exist_ok=True)

    return dirpath


def get_config_toml() -> dict:
    import os
    import tomllib

    filepath = os.path.join(get_dkdc_dir(), "config.toml")

    with open(filepath, "rb") as f:
        config = tomllib.load(f)

    return config
