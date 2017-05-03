__author__ = 'tkraus-m'

from kazoo.client import KazooClient
import datetime
import socket
import json

zk_hosts = '52.53.192.187:2181,13.56.16.80:2181,54.193.81.80:2181'
zk_port = 2181
zk_root_path = "/a-zk-test-16/host"
zk_node_name = "node"
num_paths = 2
num_nodes_per_path = 5
node_content = ' TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE BEing TESTED Check node contents TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING \
TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE being TESTED Check node contents TESTING TESTING TESTING '

def zk_write_test(zk_root_path,zk_node_name,num_paths,num_nodes_per_path,node_content):
    paths_created=[]
    start_time=datetime.datetime.now()
    for i in range(0,num_paths):
        full_zk_path = "{}/{}-{}".format(zk_root_path,'path',str(i))
        zk.ensure_path(full_zk_path)
        for j in range(0,num_nodes_per_path):
            zk.create("{}/{}-{}".format(full_zk_path,zk_node_name,j), str.encode(node_content))
            paths_created.append("{}/{}-{}".format(full_zk_path,zk_node_name,j))
    end_time=datetime.datetime.now()
    delta_time=end_time - start_time
    print("Time elapsed = " + str(delta_time) +" seconds. \n")
    return paths_created

def zk_checks(zk_host,zk_port,verb):

    host=zk_host.split(':')[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, zk_port))
    b_verb=str.encode(verb)
    s.sendall(b_verb)
    data = s.recv(1024)
    s.close()
    data=data.decode("utf-8")
    return data

if __name__ == "__main__":

    print("ZK Hosts are " + zk_hosts + "\n")

    ## RESET The STATISTICS - ONE TIME
    for zk_host in zk_hosts.split(','):
        print("Resetting stats on ZK Host # " + zk_host)
        zk_ok = zk_checks(zk_host, zk_port,'srst')
        print("Statistics reset  \n")

    # Work on ZK WRITES
    count=0
    all_host_paths=[]
    print("Number of ZK Paths to write = "+ str(num_paths))
    print("Number of ZK Nodes in each path = "+ str(num_nodes_per_path)+"\n")
    for zk_host in zk_hosts.split(','):
        print("Working on ZK Host #"+ str(count) +" , " + zk_host)
        zk = KazooClient(hosts=zk_host)
        zk.start()
        created_paths = zk_write_test('{}-{}'.format(zk_root_path,count),zk_node_name,num_paths,num_nodes_per_path,node_content)
        all_host_paths.extend(created_paths)
        count=count + 1
        zk.stop()

    # READ ZK Data
    print("Reading unprotected ZK Data back in.")
    zk = KazooClient(hosts=zk_hosts)
    zk.start()
    for zk_path in all_host_paths:
        data, stat = zk.get(zk_path)
        print("{} {}{}{}".format("ZK Node version: is ",stat.version, ".  ZK Data sample ",  data.decode("utf-8").split(' ')[:3]))
    zk.stop()

    # Get Bouncer Data
    print("Reading digest protected /bouncer/data/data.json data from zk")
    zk = KazooClient(hosts=zk_hosts)
    zk.start()
    zk.add_auth('digest','super:secret')
    data, stat = zk.get('/bouncer/datastore/data.json')
    # print("{} {}{}{}".format("ZK Version: is ",stat.version, ".\nBouncer ZK Data is \n",  data.decode("utf-8")))
    print("{} {} {}".format("Size of bouncer config is ~ ", len(data),"bytes.\n"))
    zk.stop()

    bouncer_json = json.loads(data.decode("utf-8"))

    user_count=0
    # Iterate through the bouncer_json dict
    for user in bouncer_json['users']:
        print ('Bouncer User = ' + user)
        user_count=user_count + 1

    group_count=0
    # Iterate through the bouncer_json dict
    for group in bouncer_json['groups']:
        print ('Bouncer Group = ' + group)
        group_count=group_count + 1

    acl_count=0
    # Iterate through the bouncer_json dict
    for acl in bouncer_json['acls']:
        print ('Bouncer ACLs = ' + acl)
        acl_count=acl_count + 1

    # Cleaning up test ZK Nodes
    zk = KazooClient(hosts=zk_hosts)
    zk.start()
    for i in range(0,count):
        root_path = "{}-{}".format(zk_root_path, str(i))
        print("Recursively Removing Path = " + root_path)
        zk.delete(root_path,recursive=True)
    zk.stop()
    print("\n")

    ## Work on ZK Admin & stats for Zookeeper
    host_count=0
    for zk_host in zk_hosts.split(','):
        print("Getting ZK Stats from ZK Host # "+ str(host_count) +" , " + zk_host)
        zk_ok = zk_checks(zk_host, zk_port,'ruok')
        print("ZK host "+ zk_host +" response = " + zk_ok.strip('b'))

        # Work on srvr Requests
        zk_srvr = zk_checks(zk_hosts,zk_port,'srvr')
        print(zk_srvr)
        host_count=host_count+1


    print("Total Users in Bouncer  = " + str(user_count))
    print("Total Groups in Bouncer = " + str(group_count))
    print("Total ACL's in Bouncer  = " + str(acl_count))

    '''
    # Future Work if needed
    zk_checks(zk_hosts,zk_port,'mntr')
    zk_checks(zk_hosts,zk_port,'cons')
    zk_checks(zk_hosts,zk_port,'stat')
    zk_checks(zk_hosts,zk_port,'envi')
    '''
