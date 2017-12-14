# minimum_husk

Version: v0.0.3

## The Husk Shell (experimental) - an agnostic CLI for every router.

The Husk Shell is an experimental CLI based on Napalm.  It began with the idea of
having a sngle unified console that would present the operator with a consistent 
set of commands, regardless of the Vendor.

There is very little code here, and it is simply a proof of concept. The heavy lifting all comes
from Cmd2 and Napalm. 

### Why?

- To show how awesome Napalm is. There's only about 200 lines of code to make this.
- As a proof of concecpt of a Unified Console.

While the days of direct configuration of network devices are quickly disappearing, the need
directly access the device during troubleshooting will remain.  Having a single READ ONLY 
operator console that provides a consistant interface across all devices for T1 support
may be beneficial. 	


### Cmd2

Cmd2 will provide the CLI for us, we just need to add the appropriate methods that we'd like 
in the interface

https://github.com/python-cmd2/cmd2

### Napalm

Napalm is awesome and does the majority of the work. It provides generic functions for device 
connectivity
 
https://github.com/napalm-automation/napalm

We are going to lift the majority of our help directly from Napalm


## Docker Image

[![](https://images.microbadger.com/badges/version/minimumbuilds/minimum_husk:v0.0.3.svg)](https://microbadger.com/images/minimumbuilds/minimum_husk:v0.0.3 "Get your own version badge on microbadger.com")[![](https://images.microbadger.com/badges/image/minimumbuilds/minimum_husk:v0.0.3.svg)](https://microbadger.com/images/minimumbuilds/minimum_husk:v0.0.3 "Get your own image badge on microbadger.com")[![](https://images.microbadger.com/badges/commit/minimumbuilds/minimum_husk:v0.0.3.svg)](https://microbadger.com/images/minimumbuilds/minimum_husk:v0.0.3 "Get your own commit badge on microbadger.com") 

## Build
[![Build Status](https://travis-ci.org/minimumbuilds/minimum_husk.svg?branch=v0.0.3)](https://travis-ci.org/minimumbuilds/minimum_husk)

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

This is obviously a bad idea.  In any sort of 'real' environment, all of the data in the
devices dictionary should come from other sources, like the Asset Management system.  

In any case, Husk will mark the file 

## Run
	docker run -it --rm minimumbuilds/minimum_husk

Minimal Builds. There are many like it, this one is mine.

## Built With

* [Alpine Linux](https://hub.docker.com/_/alpine/) - Alpine Linux Official Docker

## Authors

* **Minimum Builds** - *Initial work* - [minimumbuilds](https://github.com/minimumbuilds)
