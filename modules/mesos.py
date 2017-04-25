__author__ = 'tkraus'

import sys
import requests
import json
import math

class mesos(object):
    def __init__(self, dcos_master,dcos_auth_token):
        self.name = dcos_master
        self.uri='{}{}'.format(dcos_master,'/mesos')
        self.headers={'Authorization': 'token='+dcos_auth_token, 'Content-type': 'application/json'}
        # self.apps = self.get_all_apps()
        self.metrics_endpoint = '{}{}'.format(self.uri,'/metrics/snapshot')
        self.slaves_endpoint = '{}{}'.format(self.uri,'/slaves')

    def get_metrics(self):
        response = requests.get(self.uri + '/metrics/snapshot', headers=self.headers, verify=False)
        if response.status_code != 200:
            print ("Failed to get Metrics")
            return None
        else:
            #print ("Found Mesos metrics")
            return response.text

    def get_agents(self):
        response = requests.get(self.uri + '/slaves', headers=self.headers, verify=False)
        if response.status_code != 200:
            print ("Failed to get Agents")
            return None
        else:
            print ("Found Mesos Agents")
            return response.text

    def get_roles(self):
        response = requests.get(self.uri + '/roles', headers=self.headers, verify=False)
        if response.status_code != 200:
            print ("Failed to get Agents")
            return None
        else:
            #print ("Found Mesos Roles")
            return response.text
	
    def get_quota_info(self):
        response = requests.get(self.uri + '/quota', headers=self.headers, verify=False)
        if response.status_code != 200:
            print ("Failed to get Quotas")
            return None
        else:
            #print ("Found Mesos Roles")
            return response.text
 

def dcos_auth_login(dcos_master,userid,password):
    '''
    Will login to the DCOS ACS Service and RETURN A JWT TOKEN for subsequent API requests to Marathon, Mesos, etc
    '''
    rawdata = {'uid' : userid, 'password' : password}
    login_headers={'Content-type': 'application/json'}
    response = requests.post(dcos_master + '/acs/api/v1/auth/login', headers=login_headers, data=json.dumps(rawdata),verify=False).json()
    auth_token=response['token']
    return auth_token
