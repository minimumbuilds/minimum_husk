# minimum_husk

Version: v0.0.3

## Build
[![Build Status](https://travis-ci.org/minimumbuilds/minimum_husk.svg?branch=v0.0.3)](https://travis-ci.org/minimumbuilds/minimum_husk)

## The Husk Shell (experimental) - an agnostic CLI for (almost) every router.

The Husk Shell is an experimental CLI based on Napalm.  It began with the idea of
having a single unified console that would present the operator with a consistent 
set of commands, regardless of the Vendor.

There is very little code here, and it is simply a proof of concept. The heavy lifting all comes
from Cmd2 and Napalm. 

This is purely experimental project and contains bugs and bad ideas.  It is unlikely that 
this project will ever reach a 'completion' stage. 

### Why?

As a proof of concept of a Unified Console.

While the days of direct configuration of network devices are quickly disappearing, the need
directly access the device during troubleshooting will remain.  Having a single READ ONLY 
operator console that provides a consistant interface across all devices for T1 support
may be beneficial. 	

Mostly, I just did it for fun.

### Cmd2

Cmd2 will provide the CLI for us, we just need to add the appropriate methods that we'd like 
in the interface

https://github.com/python-cmd2/cmd2

### Napalm

Napalm is awesome and does the majority of the work. It provides generic functions for device 
connectivity
 
https://github.com/napalm-automation/napalm

[Currently Supported Devices:](http://napalm.readthedocs.io/en/latest/support/)

|  _    |                   EOS      |   JunOS  |         IOS-XR   |    NXOS     |     IOS|
|-|-|-|-|-|-|
 | **Module Name**      |   napalm-eos | napalm-junos  |  napalm-iosxr\ napalm-nxos |  napalm-ios|
 | **Driver Name**      |   eos        | junos         |  iosxr       \ nxos        |  ios|
 | **Structured data**  |   Yes        | Yes           |  No          \ Yes         |  No|
 | **Minimum version**  |   4.15.0F    | 12.1          |  5.1.0       | 6.1  |  12.4(20)T|
 | **Backend library**  |   pyeapi  | junos-eznc |  pyIOSXR  | pycsco   |  netmiko|

- pyeapi: https://github.com/arista-eosplus/pyeapi
- junos-eznc: https://github.com/Juniper/py-junos-eznc
- pyIOSXR: https://github.com/fooelisa/pyiosxr
- pycsco: https://github.com/jedelman8/pycsco
- netmiko: https://github.com/ktbyers/netmiko

- NX-API support on the Nexus 5k, 6k and 7k families was introduced in version 7.2

We are going to lift the majority of our help directly from Napalm

### Device contexts

Husk introduces the concept of dynamic device context to the router CLI.

**Using the device context, we are able able to issue a SINGLE command and execute it against all the 
devices in the current context, REGARDLESS of Vendor or platform.**

### Sample Video

This video shows running multiple commands across Cisco, Juniper & Arista Routers simultaneously

[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/9u4f2YOfuBk/0.jpg)](http://www.youtube.com/watch?v=9u4f2YOfuBk)
 
The following commands are run in the video


| Command   |   Function  |
|------------------------------------|---------------------------------------------------------------------------|
|?|  Help|
|help get_interfaces_ip| Command specific help |
|show_devices| Show the device Inventory | 
|set_context vsrx veos cisco-switch1 | Set the context |
|is_alive| Connectivity test against device context |:w
|help get_facts | Command Specific help |
|get_facts | Get Facts |
|help get_interfaces_ip | Command Specific help |
|get_interfaces_ip | Get Interface IPs device context |
|!cat test_script | Run shell command cat to display the file 'test_script' |
|load test_script | Run `test_script` |


## Clone 

	https://github.com/minimumbuilds/minimum_husk.git

## Setup

Currently, all the device inventory is kept in a dictionary in setup.py

	devices = {
	    'vsrx': {
		'mgmt_ip': '172.28.128.11',
		'mgmt_port': 22,
		'device_type': 'junos',
		'username': 'readonly',
		'password': 'readonly'},
	    'veos': {
		'mgmt_ip': '172.28.128.10',
		'mgmt_port': 443,
		'device_type': 'eos',
		'username': 'readonly',
		'password': 'readonly'},
	    'cisco-switch1': {
		'mgmt_ip': '192.168.1.158',
		'mgmt_port': 22,
		'device_type': 'ios',
		'username': 'readonly',
		'password': 'readonly'}
	    }

This is obviously a bad idea. (plain text passwords, eeek)

In any sort of 'real' environment, all of the data in the
devices dictionary should come from other sources, like the Asset Management system.

Husk will change the  permissions on settings.py to RW for the owner exclusively
and this will suffice for our prototype.

## Run

	python husk.py



Minimal Builds. There are many like it, this one is mine.

## Authors

* **Minimum Builds** - *Initial work* - [minimumbuilds](https://github.com/minimumbuilds)
