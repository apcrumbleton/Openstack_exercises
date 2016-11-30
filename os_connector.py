#!/usr/bin/env python3
"""Function to generate default connection object to CityCloud"""
from shade import *

def os_cc_conn():
    #simple_logging(debug=True)
    conn = openstack_cloud(cloud='citycloud')
    return conn

