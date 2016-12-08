#!/usr/bin/env python3
"""Check for and insert an ssh key pair for authenticaiton with the cloud server"""

from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

print('\nChecking for an existing SSH key pair ... \n')
keypair_name = 'bobdemokey'
pub_key_file = '/home/dale/Openstack_exercises/keys/bobtest.pub'

if conn.search_keypairs(keypair_name):
    print('Keypair already exists, Skipping import.')
else:
    print('Adding keypair ... ')
    conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

for keypair in conn.list_keypairs():
    print(keypair)

