# Some crude methods to get a more consistent 'get_ip_route' results,
# needs significant refinement to be really usable.

from jnpr.junos import Device as JunosDevice
from jnpr.junos.op.routes import RouteTable
import pyeapi
import re

import settings

from pprint import pprint as pp

def get_junos_route_table(device):
    details = settings.devices[device.name]
    dev = JunosDevice(details['mgmt_ip'], user=details['username'], passwd=details['password'], port=details['mgmt_port'])
    dev.open()
    routes = RouteTable(dev)
    routes.get()
    dev.close()
    route_list = dict([item for item in routes.items() if item[1][0][1] not in ['Local','Access-internal']])
    return(route_list)


def get_arista_route_table(device):
    details = settings.devices[device.name]
    conn = pyeapi.connect(host=details['mgmt_ip'], username=details['username'], password=details['password'], port=details['mgmt_port'])
    route_list = conn.execute(['show ip route'])['result'][0]['vrfs']['default']['routes']
    return(route_list)


def get_cisco_route_table(device):
    response = device.connector.cli(['show ip route'])
    response_list = [line for line in response['show ip route'].splitlines() if
                  re.search(r'(?:\d{1,3}\.)+(?:\d{1,3})', line)]
    route_list = {}
    for thing in response_list[1:]:
        route_list[thing.split()[1]] = [('via', " ".join(thing.split()[2:])), ('RouteType', thing.split()[0])]
    return(route_list)


def get_ip_route(context):
    for device in context:
        print()
        print('*' * 80)
        print("Running 'get_ip_route' against device: {}@{}:{}({})".format(device.name, device.mgmt_ip, device.mgmt_port,
                                                             device.device_type))
        print()
        if device.device_type == 'junos':
            response = get_junos_route_table(device)
        elif device.device_type == 'eos':
            response = get_arista_route_table(device)
        elif device.device_type == 'ios':
            response = get_cisco_route_table(device)
        else:
            response = 'Not available on this platform'
        pp(response)
    return