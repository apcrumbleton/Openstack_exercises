#!/usr/bin/env python3
"""Generate security group and rules to allow for access to the instance
    via ssh and http"""

from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

print('\nChecking for existing security groups ...\n')
sec_group_name = 'ssh_web'
if conn.search_security_groups(sec_group_name):
    print('Security group already exists. Skipping creation.')
else:
    print('Creating Security group ... ')
    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

conn.search_security_groups(sec_group_name)

