from netmiko import ConnectHandler
import yaml
import ipaddress
import sys

# def check_ospf_neighbors(ip, subnet_list):
#     i = 0
#     for subnet in subnet_list:
#         if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet_list[i]):
#             # print(ipaddress.ip_address(ip) + "------------------------>" + ipaddress.ip_network(subnet_list[i]))
#             return True  # At least one IP belongs to the subnet, stop checking
#         i+=1
#     return False  # None of the IPs belong to the subnet

def check_ospf_neighbors(ips_command, ips_file):
    def is_ip_in_subnets(ip, ips_file):
        ip_obj = ipaddress.IPv4Address(ip)
        for subnet in ips_file:
            if ip_obj in ipaddress.IPv4Network(subnet):
                return True
        return False

    return all(is_ip_in_subnets(ip, ips_file) for ip in ips_command)

def check_ospf_area():
    def is_ip_in_subnets_neigh(interface):   
        ospf_area_command = net_connect.send_command(f'show ip ospf interface {interface["name"]}', use_textfsm=True)
        ip_obj = ipaddress.IPv4Address(interface["ipv4_addr"].split('/')[0])
        if len(ospf_area_command) != 0:
            for subnet in ceos["ospf"]['networks']:
                if ip_obj in ipaddress.IPv4Network(subnet["ip"]) and subnet["area"] in ospf_area_command.split('\n')[1].split(',')[-1]:
                    return True
            return True

    return any(is_ip_in_subnets_neigh(interface) for interface in [interface for interface in ceos.get('interfaces', [])])

ip = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]
device_type = sys.argv[4]

if "arista" in device_type:
    device_type = "arista_eos"

## OSPF NEIGHBORS ##
    
net_connect = ConnectHandler(
    device_type = device_type,
    host = ip,
    username = user,
    password = password,
)

with open(f'./config_vars/{ip}.yml', 'r') as file:
    ceos = yaml.safe_load(file)

ospf_neigh = net_connect.send_command("show ip ospf neighbor", use_textfsm=True)

ospf_neigh_file = [item['ip'] for item in ceos["ospf"]['networks']]

ospf_neigh_command = [item['ip_address'] for item in ospf_neigh]

print(check_ospf_area())
print(check_ospf_neighbors(ospf_neigh_command,ospf_neigh_file))

net_connect.disconnect()