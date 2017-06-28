__author__ = 'tkraus-m'

import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from modules.dcos import *

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import argparse
import sys

'''
dcos_master = 'https://54.200.228.222'
userid = input('Enter the username for the DCOS cluster '+dcos_master +' : ')
password = input('Enter the password for the DCOS cluster '+dcos_master +' : ')
'''
print ("This application tested with Python3 only")
parser = argparse.ArgumentParser(description='Mesos Agent Resources app.')
parser.add_argument('--dcos-master', help='The DNS hostname or IP of your Marathon Instance', required=True)
parser.add_argument('--userid', help='Username for the DCOS cluster')
parser.add_argument('--password', help='Password for the DCOS cluster')

try:
    args = parser.parse_args()
except Exception as e:
    parser.print_help()
    sys.exit(1)

dcos_master = args.dcos_master
userid = args.userid
password = args.password

if userid is not None:
    dcos_auth_token = dcos_auth_login(dcos_master,userid,password)

    print('Auth Token is = ' + dcos_auth_token)
else:
    dcos_auth_token=None


## MESOS SECTION
new_mesos = mesos(dcos_master,dcos_auth_token)

mesos_stats_text = new_mesos.get_metrics()
# Change - Remove RAW print below.
# print("DEBUG - RAW Mesos stats = " + mesos_stats_text)
mesos_stats_json = json.loads(mesos_stats_text)


print ("MESOS AGENTS Resource Information")
# Agents Calculation  
mesos_agents_text = new_mesos.get_agents()
mesos_agents_json = json.loads(mesos_agents_text)


dict_for_totals_perRole={}
total_cpu_per_role=0
total_disk_per_role=0
total_mem_per_role=0

for agent in mesos_agents_json['slaves']:
    # "agent" is a dict object
    print('\n-----------------------------------------------------------------------------------------------------')
    print('{}: {}    {}: {}'.format('Agent ID',agent['id'],'Hostname',agent['hostname']))

    print(' {} = {} {}'.format('Mesos Configured CPU',int(agent.get('resources',{'cpus'})['cpus']),'Cores'))
    print(' {} = {} {}'.format('Mesos Configured MEM',int(agent.get('resources',{'mem'})['mem']) / 1000, 'GB'))
    print(' {} = {} {}'.format('Mesos Configured DISK',int(agent.get('resources',{'disk'})['disk']) / 1000, 'GB'))
    print(' {} = {}'.format('Mesos Configured GPUs',int(agent.get('resources',{'gpus'})['gpus'])))
    
    reservations = agent['reserved_resources_full']
    # reservations is a python dict
    # print('{} ={}'.format('DEBUG - Full Agent Reserved Resources Full KEY', agent['reserved_resources_full'].items()))


