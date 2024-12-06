from blissdata.beacon.data import BeaconData
from packaging.version import Version
from importlib.metadata import version

if Version(version("blissdata")) >= Version("1.1"):
    from pydantic import Field  # noqa
else:
    from pydantic.v1 import Field  # noqa


def get_redis_db_url():
    if Version(version("blissdata")) >= Version("1.0"):
        return BeaconData().get_redis_db()

    raw_url = BeaconData().get_redis_db()
    host, url = raw_url.split(":")

    if url.endswith("sock"):
        return f"unix://{url}"
    else:
        return f"redis://{url}"
