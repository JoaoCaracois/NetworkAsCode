#!/usr/bin/python3

from netmiko import ConnectHandler
import yaml
import sys
            
def check_ntp(ntp_command, ntp_file):
    return set(ntp_command) == set(ntp_file)

ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
device_type = sys.argv[4]

if "arista" in device_type:
    device_type = "arista_eos"

net_connect = ConnectHandler(
    device_type = device_type,
    host = ip,
    username = user,
    password = password,
)

with open(f'./config_vars/{ip}.yml', 'r') as file:
    ceos = yaml.safe_load(file)

get_ntp = net_connect.send_command('show ntp associations', use_textfsm=True).splitlines()[2:]
ntp_ip_command = [item.split()[0] for item in get_ntp]

print(check_ntp(ntp_ip_command, ceos['ntp_servers']))