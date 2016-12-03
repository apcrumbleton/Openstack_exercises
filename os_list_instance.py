#!/usr/bin/env python3
"""Test script to list any instances existing on our cloud server.
   useful to check if the instance was actually started and running."""

from shade import *
from os_connector import *

conn = os_cc_conn()

instances = conn.list_servers()
for instance in instances:
    print(instance)

