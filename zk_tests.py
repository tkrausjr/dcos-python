__author__ = 'tkraus-m'

from kazoo.client import KazooClient
import datetime
import socket

zk_hosts = '54.193.113.160:2181,54.215.214.63:2181,52.53.184.163:2181'
zk_port = 2181
zk_root_path = "/a-zk-test/host"
zk_node_name = "node"
num_paths = 2
num_nodes_per_path = 6
node_content = ' TESTING TESTING TESTING DCOS NODE being TESTED DCOS NODE BEing TESTED Check node contents TESTING \
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
        paths_created.append(full_zk_path)
        for j in range(0,num_nodes_per_path):
            zk.create("{}/{}-{}".format(full_zk_path,zk_node_name,j), str.encode(node_content))

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

    # Cleaning up test ZK Nodes

    #new_count=count-1
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

        '''
        zk_checks(zk_hosts,zk_port,'mntr')
        zk_checks(zk_hosts,zk_port,'cons')
        zk_checks(zk_hosts,zk_port,'stat')
        zk_checks(zk_hosts,zk_port,'envi')
        '''
