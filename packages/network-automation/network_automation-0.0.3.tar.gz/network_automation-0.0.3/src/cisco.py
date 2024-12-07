from src import environment
from mydict import MyDict
from netmiko import ConnectHandler


class CiscoSSHDevice(object):
    def __init__(self, hostname, username=None, password=None):
        self.hostname = hostname
        self.username = username or environment.get_cisco_username()
        self.password = password or environment.get_cisco_password()

        if environment.VERBOSE:
            print(f"Cisco username: {self.username}")

        netmiko_device = {
            'device_type': "cisco_ios",
            'ip': self.hostname,
            'username': self.username,
            'password': self.password,
            'secret': self.password,
        }
        self.conn = ConnectHandler(**netmiko_device)

    def execute_command(self, command):
        return self.conn.send_command(command, use_textfsm=True)

    def get_interface_details(self):
        interfaces = self.execute_command('show interface')
        return [MyDict(x) for x in interfaces]

    def get_device_serial(self):
        serial = self.conn.send_command('show version | include Processor')
        return serial.split(' ')[-1]
