import pynetbox
from src.netbox import NetBoxInstance


def test_get_netbox():
    netbox = NetBoxInstance(
        "https://netbox.example.com/",
        token="1234567890",
    )
    assert isinstance(netbox, pynetbox.api)
