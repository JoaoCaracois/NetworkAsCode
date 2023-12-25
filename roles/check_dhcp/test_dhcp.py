#!/usr/bin/python3

from netmiko import ConnectHandler
import yaml
import sys
            
def check_dhcp_server(dhcp_command, dhcp_file):
    for dict1 in dhcp_command:
        for dict2 in dhcp_file:
            if dict1['subnet'] in dict2['network'] and dict1['default-gateway'] in dict2['gateway'] and dict2['start'] in dict1['range'] and dict2['end'] in dict1['range'] and dict2['lease'] in dict1['lease'] and all(item in dict1['dns'] for item in dict2['dns_server']):
                return True
    return False
            
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

net_connect.enable()
get_dhcp_server = net_connect.send_command('show run section dhcp server | grep -v -e "interface" -e "ipv4" -e "dhcp"')

subnet_configs = [config.strip() for config in get_dhcp_server.split('!') if config.strip()]

subnet_info_list = []

for config in subnet_configs:
    config_lines = config.strip().split('\n')
    subnet_info_dict = {}

    for line in config_lines:
        key, *value = line.split()
        value = ' '.join(value)
        subnet_info_dict[key] = value

    subnet_info_list.append(subnet_info_dict)

print(check_dhcp_server(subnet_info_list, ceos['dhcp']['subnets']))