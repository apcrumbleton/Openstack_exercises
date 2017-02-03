#!/usr/bin/env python3
"""FINAL script to instantiate a running server and have it accessible
    via the ssh and http service ports and eventually generate fractals
    """

from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

# Get the image ID and flavor ID from the previous scripts:
# os_create_instance_TEST.py, os_shade_01.py
flavor_id = '5a10e223-aada-4d5a-8633-84525e05b28f'
image_id = '517335db-ebff-4d33-befc-8200cd7c7093'
instance_name = 'bobs_test_instance'

# Get the key pair name and security group name from previous scripts:
# os_keypairs.py, os_security_group.py
keypair_name = 'bobdemokey'
sec_group_name = 'ssh_web'

# Define the special bit from the fractal application devleopers that will ensure that all the pieces are in place on the instantiated server:
ex_userdata = '''#!/usr/bin/env bash

curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

# Define the FINAL instance that will hold everything:
##instance_name = 'all-in-one' ## SEE ABOVE for MY instance name
testing_instance = conn.create_server(wait=True, auto_ip=False,
        name=instance_name,
        image=image_id,
        flavor=flavor_id,
        key_name=keypair_name,
        security_groups=[sec_group_name],
        userdata=ex_userdata)

## NOTE: the above option "auto_ip=False", means we HAVE TO request and then
##       assign a floating IP address for PUBLIC IP access.
##       In the previous example script "os_create_instance_TEST.py" the
##       IP address was AUTOMATICALLY assigned!
# The next bit attempts to manually assign the IP
# find an available floating IP:
f_ip = conn.available_floating_ip()
# assign this IP to the instance:
conn.add_ip_list(testing_instance, [f_ip['floating_ip_address']])
# print a message to show the address at which the application may be available:
print('The Fractals app will be deployed to http://%s' % f_ip['floating_ip_address'] )
#
## Our instance SHOULD have an auto-assigned and INTERNET accessible IP
## SO, show the whole instance data and see if it's there:
#instances = conn.list_servers()
#for instance in instances:
#    print(instance)

