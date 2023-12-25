#!/usr/bin/python3

from netmiko import ConnectHandler
import yaml
import sys

def check_bgp_neighbors_ip(neighbors_ip_command,neigh_ip_file):
    if not any(item in neigh_ip_file for item in neighbors_ip_command):
        return False
    return True

def check_bgp_neighbors_as(neighbors_as_command,neigh_as_file):
    if not any(item in neigh_as_file for item in neighbors_as_command):
        return False
    return True

def check_bgp_neighbors_state(neighbors_state_command):
    return all(item == 'Estab' for item in neighbors_state_command)

def check_number_of_neighbors(neighbor_number_command, neighbor_number_file):
    return len(neighbor_number_command) == len(neighbor_number_file)


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

get_bgp_sessions = net_connect.send_command("show ip bgp summary", use_textfsm=True)

neigh_list_ip_file = [item['ipv4_addr'] for item in ceos["bgp"]["neighbors"]]
neigh_list_as_file = [item['AS'] for item in ceos["bgp"]["neighbors"]]
neigh_list_as_file = [str(item) for item in neigh_list_as_file]

neigh_ip_command = [item['bgp_neigh'] for item in get_bgp_sessions]
neigh_as_command = [item['neigh_as'] for item in get_bgp_sessions]
neigh_state_command = [item['state'] for item in get_bgp_sessions]

print(check_bgp_neighbors_ip(neigh_ip_command, neigh_list_ip_file))
print(check_bgp_neighbors_as(neigh_as_command, neigh_list_as_file))
print(check_bgp_neighbors_state(neigh_state_command))
print(check_number_of_neighbors(get_bgp_sessions, neigh_list_ip_file))