import os

from dotenv import load_dotenv
from mydict import MyDict
from netmiko import ConnectHandler

load_dotenv()

cisco_username = os.environ.get("CISCO_USERNAME")
cisco_password = os.environ.get("CISCO_PASSWORD")


class CiscoSSHDevice(object):
    def __init__(self, hostname):
        self.hostname = hostname
        self.username = cisco_username
        self.password = cisco_password

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
