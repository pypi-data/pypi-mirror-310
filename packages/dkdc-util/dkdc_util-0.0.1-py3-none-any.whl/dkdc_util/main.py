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


def get_dkdc_dir():
    import os

    dirpath = os.path.join(os.path.expanduser("~"), ".dkdc")

    os.makedirs(dirpath, exist_ok=True)

    return dirpath


def load_env() -> None:
    import os

    from dotenv import load_dotenv

    load_dotenv()
    load_dotenv(os.path.join(os.getcwd(), ".env"))
    load_dotenv(os.path.join(os.path.expanduser("~"), ".env"))
    load_dotenv(os.path.join(get_dkdc_dir(), ".env"))
