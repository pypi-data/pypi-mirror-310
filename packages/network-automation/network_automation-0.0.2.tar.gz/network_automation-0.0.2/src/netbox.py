import os

from collections import defaultdict
from dotenv import load_dotenv
from pynetbox import api as netbox_api

load_dotenv()

netbox_token = os.environ.get('NETBOX_TOKEN')
netbox_url = os.environ.get('NETBOX_URL')


class NetBoxInstance(netbox_api):
    def __init__(self, url=None, token=None):
        self.url = url or netbox_url
        self.token = token or netbox_token

        super(NetBoxInstance, self).__init__(url=self.url, token=self.token)

    def duplicated_device_serials(self):
        duplicates = []
        seen_values = defaultdict(list)

        for entry in [x for x in self.dcim.devices.all() if x.serial]:
            serial = entry['serial']
            if seen_values[serial]:
                duplicates.extend(seen_values[serial])
            else:
                seen_values[serial].append(entry['serial'])

        return duplicates

    def get_all_devices(self):
        return [x for x in self.dcim.devices.all()]
