#!/usr/bin/env python3
"""Create an openstack cloud instance using a provided flavor and image
   Then print out the new instance
   Then remove it!
   (Cloud resources cost money!!)"""

from shade import *
from os_connector import *

# Get a connection object from the os_connector:
conn = os_cc_conn()

# Define variables for the chosen flavor, image and name of the new instance:
flavor_id = '5a10e223-aada-4d5a-8633-84525e05b28f'
image_id = 'cd498f49-6766-4bba-82bd-5433d3656b84'
instance_name = 'bobs_test_instance'

# spawn the instance with the above information:
testing_instance = conn.create_server(wait=True, auto_ip=True,
        name=instance_name,
        image=image_id,
        flavor=flavor_id)
print(testing_instance)

# show the created instance/server:
instances = conn.list_servers()
for instance in instances:
    print(instance)

# finally, DELETE the test instance (Cloud resources cost money!!):
#conn.delete_server(name_or_id=instance_name)
