#!/usr/bin/env python3
"""Quick script to delete a single cloud server instance on citycloud
   (Cloud resources cost money!!)"""

from shade import *
from os_connector import *

conn = os_cc_conn()

# Security groups to remove:
worker_group_name = 'worker'
controller_group_name = 'control'

conn.delete_security_group(worker_group_name)
conn.delete_security_group(controller_group_name)

# Statically named instance to remove:
name='app-controller'
conn.delete_server(name_or_id=name)
name='app-worker-1'
conn.delete_server(name_or_id=name)

