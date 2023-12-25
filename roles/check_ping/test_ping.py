from netmiko import ConnectHandler
import sys
import re

def check_packet_loss(neighbors):
    for neighbor in neighbors:
        ping_lldp_neigh = net_connect.send_command(f'ping {neighbor}')#.split('\n')[8]
        packet_loss_percentages = [int(match.group(1)) for match in re.finditer(r"(\d+)% packet loss", ping_lldp_neigh)]
        if packet_loss_percentages[0] == 100:
                    return False
    return True

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

get_lldp_neigh = net_connect.send_command("show lldp neighbors detail", use_textfsm=True)

neighbors = list(set([item['mgmt_address'] for item in get_lldp_neigh]))
print(neighbors)
print(check_packet_loss(neighbors))

net_connect.disconnect()