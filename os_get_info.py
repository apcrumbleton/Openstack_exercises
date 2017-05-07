#!/usr/bin/env python3
"""Get some info about existing (running) instances"""

from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

# LOCAL NAME:
instance_name = 'mand001'

# show the created instance/server:
instance = conn.get_server(name_or_id=instance_name)
print("\n Public IP of server : "+ instance_name + " : "+instance.interface_ip+"\n")

