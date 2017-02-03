#!/usr/bin/env python3
"""script to instantiate both a running control server and worker node
    and have the control server accessible via ssh and http ports, while
    the worker node is accessible via ssh only
    orders for fractals are initiated on the control server and fulfilled
    by the worker node
    """

import sys
from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

# Get the image ID and flavor ID from the previous scripts:
# os_create_instance_TEST.py, os_shade_01.py
flavor_id = '5a10e223-aada-4d5a-8633-84525e05b28f'
image_id = '517335db-ebff-4d33-befc-8200cd7c7093'
# NOTE: the instance_name is NOT predefined now as we will have MULTIPLE
# instance (well, only two this time but we are working upwards)
#instance_name = 

# Set the key pair name
# (from os_keypairs.py)
keypair_name = 'bobdemokey'

#+++++++++++++++++ SECURITY GROUPS +++++++++++++++++

# For the WORKER only SSH access is required:
worker_group_name = 'worker'
if conn.search_security_groups(worker_group_name):
    print('Security group',worker_group_name,' already exists, skipping creation.')
else:
    worker_group = conn.create_security_group(worker_group_name, 'for services that run on a worker node.')
    conn.create_security_group_rule(worker_group['name'], 22, 22, 'TCP')
#------------------------------------------------

# For the CONTROL server BOTH SSH and HTTP are required:
controller_group_name = 'control'
if conn.search_security_groups(controller_group_name):
    print('Security group',controller_group_name,' already exists, skipping creation.')
else:
    controller_group = conn.create_security_group(controller_group_name, 'for services that run on a controller node.')
    conn.create_security_group_rule(controller_group['name'], 22, 22, 'TCP')
    conn.create_security_group_rule(controller_group['name'], 80, 80, 'TCP')
    conn.create_security_group_rule(controller_group['name'], 5672, 5672, 'TCP', remote_group_id=worker_group['id'])
#------------------------------------------------


#+++++++++++++++++ INSTANTIATE CONTROL SERVER +++++++++++++++++
# Define the special bit from the fractal application developers that will ensure that all the pieces are in place on the instantiated control server:
controller_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api
'''

# Define the FINAL instance that will run the control server:
##instance_name = 'all-in-one' ## SEE ABOVE for MY instance name
instance_controller_1 = conn.create_server(wait=True, auto_ip=False,
        name='app-controller',
        image=image_id,
        flavor=flavor_id,
        key_name=keypair_name,
        security_groups=[controller_group_name],
        userdata=controller_userdata)

## NOTE: the above option "auto_ip=False", means we HAVE TO request and then
##       assign a floating IP address for PUBLIC IP access.
##       In the previous example script "os_create_instance_TEST.py" the
##       IP address was AUTOMATICALLY assigned!
# The next bit attempts to manually assign the IP
# find an available floating IP:
unused_floating_ip = conn.available_floating_ip()
# assign this IP to the instance:
conn.add_ip_list(instance_controller_1, [unused_floating_ip['floating_ip_address']])
# print a message to show the address at which the application may be available:
print('The Fractals app controller will be deployed to http://', unused_floating_ip['floating_ip_address'] )
#
#------------------------------------------------

# Obtain the INSTANCE ID for the new controller node:
instance_controller_1 = conn.get_server(instance_controller_1['id'])
# Obtain the public IP of the controller node using the ID value above:
#if conn.get_server_public_ip(instance_controller_1):
#    ip_controller = conn.get_server_public_ip(instance_controller_1)
#else:
#    ip_controller = conn.get_server_private_ip(instance_controller_1)
# NOTE: Obtaining ONLY the PRIVATE IP of the controller here, since
# from initial use, the PUBLIC IP did not work for passing messages
# between the controller and the worker, BUT entering the PRIVATE
# IP addresses in the WORKER configuraiton DID work.
ip_controller = conn.get_server_private_ip(instance_controller_1)
#------------------------------------------------

#+++++++++++++++++ INSTANTIATE WORKER NODE +++++++++++++++++
# Define the special bit from the fractal application developers that will ensure that all the pieces are in place on the instantiated worker node:
worker_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -r worker -e 'http://%(ip_controller)s' -m 'amqp://guest:guest@%(ip_controller)s:5672/'
''' % {'ip_controller': ip_controller}

# Define the FINAL worker instance that will take requests from the controller:
instance_worker_1 = conn.create_server(wait=True, auto_ip=False,
        name='app-worker-1',
        image=image_id,
        flavor=flavor_id,
        key_name=keypair_name,
        security_groups=[worker_group_name],
        userdata=worker_userdata)
# find an available floating IP:
unused_floating_ip = conn.available_floating_ip()
# assign this IP to the instance:
conn.add_ip_list(instance_worker_1, [unused_floating_ip['floating_ip_address']])
# print a message to show the address at which the application may be available:
print('The Fractals app worker will be available via SSH at', unused_floating_ip['floating_ip_address'] )
#------------------------------------------------

