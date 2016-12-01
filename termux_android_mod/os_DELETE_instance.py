#!/data/data/com.termux/files/usr/bin/env python3
"""Quick script to delete a single cloud server instance on citycloud
   (Cloud resources cost money!!)"""

from shade import *
from os_connector import *

conn = os_cc_conn()

# Statically named instance to remove:
instance_name = 'bobs_test_instance'

conn.delete_server(name_or_id=instance_name)

