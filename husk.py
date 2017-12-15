# Import stuff

# napalm - handles all our device communications
# We'll pull our methods & docstrings from napalm_base
import napalm
import napalm_base
import napalm_base.exceptions
from napalm._SUPPORTED_DRIVERS import SUPPORTED_DRIVERS


import importlib
import getpass
import os
from pprint import pprint as pp
from ipaddress import ip_address

# cmd2 provides the CLI, history, autocompletion, help, etc..
from cmd2 import Cmd

# Defining a command not in Napalm
from get_ip_route import get_ip_route

import settings
os.chmod('settings.py', 384)


class Device:
    # Device class to hold our connectors and details
    def __init__(self, hostname):
        details = settings.devices[hostname]

        driver = napalm.get_network_driver(details['device_type'])
        device = driver(hostname=details['mgmt_ip'],
                        username=details['username'], password=details['password'],
                        optional_args={'port': details['mgmt_port']})
        device.open()

        self.name = hostname
        self.device_type = details['device_type']
        self.mgmt_ip = details['mgmt_ip']
        self.mgmt_port = details['mgmt_port']

        self.connector = device

    def __repr__(self):
        return (self.name)

    def __str__(self):
        return (self.name)


def get_docs(method):
    # Returns the docstring for NetworkDriver method
    return getattr(napalm.base.NetworkDriver, method.strip()).__doc__


class MyCmd(Cmd):
    # Set our device context
    context = []
    prompt = "Context:{}>".format(str(context))

    def precmd(self, arg):
        """
        Before command execution:

        - Check if command is 'help'
        - if 'help', then get the docstring from napalm for the command
        - replace the docstring in fake_command with the docstring from napalm
        """

        if 'help' in arg.parsed[0]:
            method = arg.parsed[1]
            if method != '':
                try:
                    fake_command.__doc__ = get_docs(method)
                except:
                    # TODO...
                    fake_command.__doc__ = "No help available, sorry"

        return(arg)

    def postcmd(self, stop, line):
        if self.context == []:
            print("Context is empty, use 'set_context' to add/remove devices to current context")

    def do_exit(self, arg):
        return True

    def do_quit(self, arg):
        return True

    def do_set_context(self, arg):
        """
        Specify the current context.

        usage: prompt>set_context <device_name> <device_name> ...
        """
        new_context = arg.split()
        for device in self.context:
            if device.name not in new_context:
                device.connector.close()

        # remove not in list
        self.context = [x for x in self.context if x.name in new_context]

        # get a list of names in the current context for comparison
        context_list = [x.name for x in self.context]

        # add any new settings.devices to the context
        self.context += [Device(new_device) for new_device in new_context if new_device not in context_list]
        self.prompt = "Context:{}>".format(str(self.context))

    def complete_set_context(self, text, line, begidx, endidx):
        """
        tab-completion method for do_set_context()
        """
        return [i for i in settings.devices.keys() if i.startswith(text)]

    def do_refresh_inventory(self, arg):
        """
        Refresh Device inventory

        usage: prompt>refresh_inventory
        """
        importlib.reload(settings)

    def do_get_ip_route(self, arg):
        """
        Returns a dictionary of routes and associated details.

        Currently provides inconsistent results per vendor:

        Example::

        {'10.0.2.0/24': [('protocol', 'Direct'),
                 ('via', 'ge-0/0/0.0'),
                 ('age', 161670),
                 ('nexthop', None)],
         '192.168.57.0/24': [('protocol', 'Direct'),
                     ('via', 'ge-0/0/1.0'),
                     ('age', 95313),

        """
        get_ip_route(self.context)

    def do_add_device(self, args):
        """
        Add a new device to inventory.
        """
        if args:
            # {'junos-vsrx1': {'mgmt_ip': '192.168.1.181', 'mgmt_port': 2202,
            # 'device_type': 'junos', 'username': 'readonly', 'password': 'readonly'}}
            pass
        else:
            print('Add new device:')
            name = input('{}>'.format('name'))

            while True:
                try:
                    mgmt_ip = input('{}>'.format('mgmt_ip'))
                    ip_address(mgmt_ip)
                except ValueError:
                    print("Invalid IP address.")
                    continue
                else:
                    break

            while True:
                mgmt_port = input('{}>'.format('mgmt_port'))
                if not 1 <= int(mgmt_port) <= 65535:
                    print('Invalid port (1-65535)')
                else:
                    break

            while True:
                print('Supported device types: {}'.format(SUPPORTED_DRIVERS))
                device_type = input('{}>'.format('device_type'))
                if device_type not in SUPPORTED_DRIVERS:
                    print('Invalid device type')
                else:
                    break

            username = input('{}>'.format('username'))
            password = getpass.getpass()

        new_device_list = settings.devices

        new_device_list[name] = {
            'mgmt_ip': mgmt_ip,
            'mgmt_port': mgmt_port,
            'device_type': device_type,
            'username': username,
            'password': password,
        }

        with open('settings.py', 'w') as f:
            f.write("devices = {}".format(str(new_device_list)))

        importlib.reload(settings)

    def do_delete_device(self, *args):
        """
        Deletes a device from inventory

        :param self:
        :param args:
        :return:
        """
        new_device_list = settings.devices
        changed = False
        for item in args:
            if item == '':
                pass
            elif item in new_device_list.keys():
                if input('Are you sure you want to delete {}?'.format(item)).lower() == 'y':
                    if new_device_list.pop(item):
                        changed = True
                        print('Deleted:{}'.format(item))
            else:
                print('{} not found'.format(item))
        if changed:
            with open('settings.py', 'w') as f:
                f.write("devices = {}".format(str(new_device_list)))
            importlib.reload(settings)

    def complete_delete_device(self, text, line, begidx, endidx):
        return [i for i in settings.devices.keys() if i.startswith(text)]

    def do_show_devices(self, args):
        """
        Show device inventory

        :param args:
        :return:
        """
        for device in list(settings.devices.keys()):
            print(device)


def fake_command(self, arg):
    """
    This is our primary method in the CLI.  Using setattr, we will map a new method under the 'MyCmd'
    class for each method in napalm_base we want to expose in the CLI, using the name of the method from napalm_base
    with the prefix 'do_'.

    Normally, you would add the methods under the class directly, as shown in 'do_context(),
    etc..

    :param self:
    :param arg:
    :return:
    """

    # invoke device.connector.<method>(*args) using getattr
    def run_command(device, connector):
        return getattr(device.connector, connector)()

    # grab the first word in the input
    this_command = arg.parsed[0]

    # Run against each device in the inventory, sequentially...
    for my_device in self.context:
        print()
        print('*' * 80)
        print("Running '{}' on device: {}@{}:{}({})".format(this_command,
                                                            my_device.name,
                                                            my_device.mgmt_ip,
                                                            my_device.mgmt_port,
                                                            my_device.device_type))
        print()
        try:
            output = run_command(my_device, this_command)
        except NotImplementedError as e:
            print('Command not implemented for this platform', e)
            continue

        # Print(output)
        if this_command == 'get_config':
            # This output could be a little prettier, should paginate
            print(output['running'])
        else:
            pp(output)
        print()


if __name__ == "__main__":
    """
    ___main___
    """

    intro = """
                                            Welcome the Husk Shell!

    Husk is a proof of concept for a vendor neutral management console, primarily based on the awesome napalm library.

    The CLI, including tab-completion and history, is all provided by the cmd2.

    https://github.com/napalm-automation/napalm
    https://github.com/python-cmd2/cmd2


    Type "help" to get started.

    """

    print(intro)

    # Get a list of methods from NetworkDriver that we want to expose.

    #   Grab specific command only
    specified_commands = ['is_alive', 'get_arp_table', 'get_config', 'get_facts', 'get_interfaces',
                          'get_interfaces_counters', 'get_interfaces_ip', 'get_mac_address_table']
    commands = [func for func in dir(napalm.base.NetworkDriver) if
                callable(getattr(napalm.base.NetworkDriver, func)) and func in specified_commands]

    """
    (alternative) Grab all 'get' methods as well additional specified

    additional_commands = ['is_alive',
                           'compare_config',
                           'commit_config',
                           'discard_config',
                           'load_merge_candidate',
                           'load_replace_candidate',
                           'ping',
                           'traceroute']
    commands = [func for func in dir(napalm.base.NetworkDriver) if
        callable(getattr(napalm.base.NetworkDriver, func)) and
            (func.startswith("get") or func in additional_commands)]

    This will produce significantly more commands on the CLI.

    Documented commands (type help <topic>):
    =======================================
    relative_load            get_interfaces_ip          is_alive
    add_device                get_ip_route               load
    cmdenvironment            get_ipv6_neighbors_table   load_merge_candidate
    commit_config             get_lldp_neighbors         load_replace_candidate
    compare_config            get_lldp_neighbors_detail  ping
    delete_device             get_mac_address_table      py
    discard_config            get_network_instances      pyscript
    edit                      get_ntp_peers              refresh_inventory
    get_arp_table             get_ntp_servers            run
    get_bgp_config            get_ntp_stats              save              i
    get_bgp_neighbors         get_optics                 set
    get_bgp_neighbors_detail  get_probes_config          set_context
    get_config                get_probes_results         shell
    get_environment           get_route_to               shortcuts
    get_facts                 get_snmp_information       show
    get_firewall_policies     get_users                  show_devices
    get_interfaces            help                       traceroute
    get_interfaces_counters   history

    Undocumented commands:
    ======================
    exit  quit
    """


# For each method, create a method named "'do_'+method name" under MyCMD,
# and map that to 'my_list_runne

    for method in commands:
        fake_command.__doc__ = 'place holder'  # Add a placeholder doc so cmd2 will show in help menu

        setattr(MyCmd, 'do_{}'.format(method),  fake_command)

    # Launch the CLI
    target = MyCmd()
    target.cmdloop()
