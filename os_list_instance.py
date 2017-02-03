#!/usr/bin/env python3
"""Test script to list any instances existing on our cloud server.
   useful to check if the instance was actually started and running."""

from shade import *
from os_connector import *

conn = os_cc_conn()

instances = conn.list_servers()
print('ALL INFO:')
for instance in instances:
    print(instance)

print('')
print('SUMMARY, Name, IP addresses and ID only:')
print('========================================')
for instance in instances:
    ip_private = conn.get_server_private_ip(instance)
    ip_public = conn.get_server_public_ip(instance)
    id_instance = (instance['id'])
    print('Name:', instance['name'], 'Private:',ip_private, 'Public:', ip_public, 'ID:',id_instance)


