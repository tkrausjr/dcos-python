__author__ = 'tkraus-m'

from kazoo.client import KazooClient

DCOS_ZK_HOSTS='34.209.193.126:2181,52.25.154.122:2181,34.210.105.168:2181,52.42.117.249:2181,52.40.252.87:2181'

DCOS_ZK_AUTH_TYPE='digest'
DCOS_ZK_CREDS='super:secret'
DCOS_ZK_AUTH_DATA=[(DCOS_ZK_AUTH_TYPE, DCOS_ZK_CREDS)]

DCOS_BOUNCER_LOCK_PATH='/bouncer/datastore/locking'
DCOS_BOUNCER_DATA_PATH='/bouncer/datastore/data.json'

DCOS_BOUNCER_DATA_FILE='/Users/tkraus/Downloads/bouncer-datastore-data.json'

zk = KazooClient(hosts=DCOS_ZK_HOSTS, auth_data=DCOS_ZK_AUTH_DATA)
zk.start()
if zk.exists(DCOS_BOUNCER_DATA_PATH):
    with open(DCOS_BOUNCER_DATA_FILE) as f:
        with zk.Lock(DCOS_BOUNCER_LOCK_PATH):
            zk.set(DCOS_BOUNCER_DATA_PATH, f.read().encode())
            data, stat = zk.get(DCOS_BOUNCER_DATA_PATH)
    print(data.decode())
    print(stat)
zk.stop()