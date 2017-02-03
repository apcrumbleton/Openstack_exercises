#!/usr/bin/env python3
"""Test program to get and list available images within a cloud"""

#import pprint
import sys
from shade import *
from os_connector import *

#simple_logging(debug=True)
#conn = openstack_cloud(cloud='citycloud')
conn = os_cc_conn()

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(conn)
#pprint.pprint(decode((conn))

images = conn.list_images()
for image in images:
#    #print(image)
    print("Name: "+image['name']+"\n"+"ID: "+image['id']+"\n"+"Size (bytes??): "
            +repr(image['size'])+"\n"+"Min RAM: "+repr(image['minRam'])+"\n")
sys.exit(0)

## An Ubuntu image:
#Name: Ubuntu 16.04 Xenial Xerus
#ID: cd498f49-6766-4bba-82bd-5433d3656b84
#Size (bytes??): 303235072
#Min RAM: 0
#
## A Debian image:
#Name: Debian 8.5
#ID: 3c7a552d-aec6-454d-8620-f3e9cbc0cdda
#Size (bytes??): 485465600
#Min RAM: 0
#

# BE PATIENT, THIS TAKES QUITE SOME TIME: (seems to loop endlessly, but does not)
#flavors = conn.list_flavors()
#for flavor in flavors:
#    #print(flavor)
#    print("Name: "+flavor['name']+"\n"+"ID: "+flavor['id']+"\n"+"CPUs: "
#            +repr(flavor['vcpus'])+"\n"+"RAM: "+repr(flavor['ram'])+"\n"+"Disk: "
#            +repr(flavor['disk'])+"\n")

## A small FLAVOR:
#Name: 1C-1GB-100GB
#ID: 5a10e223-aada-4d5a-8633-84525e05b28f
#CPUs: 1
#RAM: 1024
#Disk: 100
flavor_id = '5a10e223-aada-4d5a-8633-84525e05b28f'
flavor = conn.get_flavor(flavor_id)
print(flavor)

image_id = 'cd498f49-6766-4bba-82bd-5433d3656b84'
image = conn.get_image(image_id)
print(image)

