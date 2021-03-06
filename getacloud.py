#!/usr/bin/env python3
""" Getting information about ALL the clouds listed in the "clouds.yaml" file in current directory. """

import os_client_config

cloud_config = os_client_config.OpenStackConfig().get_all_clouds()
for cloud in cloud_config:
    print('\n Cloud Name: ' + cloud.name + '\n', 'Cloud Region: ' + cloud.region + '\n', 'Cloud configuration follows: \n', cloud.config, '\n')
    
