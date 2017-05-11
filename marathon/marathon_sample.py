__author__ = 'tkraus-m'

from modules import dcos

dcos_master = 'https://54.200.228.222'
userid = 'admindcos'
password = 'dcos123'
'''
dcos_master = 'https://54.200.228.222'
userid = input('Enter the username for the DCOS cluster '+dcos_master +' : ')
password = input('Enter the password for the DCOS cluster '+dcos_master +' : ')
'''
marathon_app_json = '/Users/tkraus/sandbox/marathon/12b-siege.json'

## Login to DCOS to retrieve an API TOKEN
dcos_token = dcos.dcos_auth_login(dcos_master,userid,password)
if dcos_token != '':
    print('{}{}'.format("DCOS TOKEN = ", dcos_token))
else:
    exit(1)
print('-----------------------------')

## Initialize new Marathon Instance of Marathon Class
new_marathon = dcos.marathon(dcos_master,dcos_token)

## List Marathon Apps Method
marathon_apps = new_marathon.get_all_apps()
print ("The following apps exist in Marathon...", marathon_apps)
print('-----------------------------')

## Get Marathon App Details Method - List Tasks & Agents for all Marathon Apps
if marathon_apps != None:
    for app in marathon_apps:
        app_details = new_marathon.get_app_details(app)
        print('{}{}'.format("Marathon App details = ", app_details))
        print('-----------------------------')

new_app = new_marathon.add_app(marathon_app_json)
print('Marathon App ID is ' + new_app)
