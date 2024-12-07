from src import environment
from collections import defaultdict
from pynetbox import api as netbox_api


class NetBoxInstance(netbox_api):
    def __init__(self, url=None, token=None):
        self.url = url or environment.get_netbox_url()
        self.token = token or environment.get_netbox_token()

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
