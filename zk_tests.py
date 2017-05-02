__author__ = 'tkraus-m'

from kazoo.client import KazooClient
import datetime
import socket

zk_hosts = '54.193.113.160:2181,54.215.214.63:2181,52.53.184.163:2181'
zk_port = 2181
zk_root_path = "/a-host"
zk_node_name = "test-node"
num_paths = 2
num_nodes_per_path = 2

print(zk_hosts)

def zk_write_test(zk_root_path,zk_node_name,num_paths,num_nodes_per_path):
    start_time=datetime.datetime.now()
    for i in range(0,num_paths):
        full_zk_path = "{}/{}-{}".format(zk_root_path,'path',str(i))
        zk.ensure_path(full_zk_path)
        for j in range(0,num_nodes_per_path):
            zk.create("{}/{}-{}".format(full_zk_path,zk_node_name,j), b"ITESTING !")
    end_time=datetime.datetime.now()
    delta_time=end_time - start_time
    print("Time elapsed = " + str(delta_time) +" seconds. \n")

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

    # Work on ZK WRITES
    count=0
    for zk_host in zk_hosts.split(','):
        print("Working on ZK Host # "+ str(count) +" , " + zk_host)
        print("Number of ZK Paths = "+ str(num_paths))
        print("Number of ZK Nodes in each path = "+ str(num_nodes_per_path))
        zk = KazooClient(hosts=zk_host)
        zk.start()
        zk_write_test('{}-{}'.format(zk_root_path,count),zk_node_name,num_paths,num_nodes_per_path)
        count=count + 1
        zk.stop()

    # Cleaning up test ZK Nodes
    '''
    count=0
    for zk_host in zk_hosts.split(','):
        print("Cleaning up ZK Host # "+ str(count) +" , " + zk_host)
        print("Recursively deleting ZK Path = "+ '{}-{}'.format(zk_root_path,count))
        zk = KazooClient(hosts=zk_host)
        zk.start()
        zk.delete('{}-{}'.format(zk_root_path,count),recursive=True)
        count=count + 1
        zk.stop()
    '''

    host_count=0
    ## Work on ZK Admin & stats for Zookeeper
    for zk_host in zk_hosts.split(','):
        print("Working on ZK Host # "+ str(host_count) +" , " + zk_host)
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
