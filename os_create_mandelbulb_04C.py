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
#Name: 4C-6GB-20GB (CPU-RAM-DISK)
flavor_id = 'a48bc83d-885c-48a6-9057-8dfc859648a0'
#
#Image: openSUSE 13.2
image_id = '7e93e4e0-31be-4b59-a750-fddb35797039'
#
# LOCAL NAME:
instance_name = 'mand001'

# Define security data: key pair and security groups:
keypair_name = 'bobdemokey'
sec_group_name = 'ssh_mandel'

# spawn the instance with the above information:
instance = conn.create_server(wait=True, auto_ip=True,
        name=instance_name,
        image=image_id,
        flavor=flavor_id,
	key_name=keypair_name,
	security_groups=[sec_group_name])

# show the created instance/server:
instances = conn.list_servers()
for instance in instances:
    print(instance)

# finally, DELETE the test instance (Cloud resources cost money!!):
#conn.delete_server(name_or_id=instance_name)
