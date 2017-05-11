from kazoo.client import KazooClient

DCOS_ZK_HOSTS='54.245.195.3:2181, 54.200.228.222:2181, 54.191.236.84:2181'

DCOS_ZK_AUTH_TYPE='digest'
DCOS_ZK_CREDS='super:secret'
DCOS_ZK_AUTH_DATA=[(DCOS_ZK_AUTH_TYPE, DCOS_ZK_CREDS)]

DCOS_BOUNCER_LOCK_PATH='/bouncer/datastore/locking'
DCOS_BOUNCER_DATA_PATH='/bouncer/datastore/data.json'

DCOS_BOUNCER_DATA_FILE='jpmc-na-2c-bouncer-datastore-data.json'

zk = KazooClient(hosts=DCOS_ZK_HOSTS, auth_data=DCOS_ZK_AUTH_DATA)
zk.start()
if zk.exists(DCOS_BOUNCER_DATA_PATH):
    with open(DCOS_BOUNCER_DATA_FILE) as f:
    	zk.set(DCOS_BOUNCER_DATA_PATH, f.read().encode())
    	data, stat = zk.get(DCOS_BOUNCER_DATA_PATH)
    print(data.decode())
    print(stat)
    zk.stop()
else:
    print(DCOS_BOUNCER_DATA_PATH + "does not exist")
    zk.stop()

