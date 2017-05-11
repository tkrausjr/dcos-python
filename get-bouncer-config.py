from kazoo.client import KazooClient

DCOS_ZK_HOSTS='54.203.197.80:2181,54.200.252.38:2181,54.149.71.163:2181'

DCOS_ZK_AUTH_TYPE='digest'
DCOS_ZK_CREDS='super:secret'
DCOS_ZK_AUTH_DATA=[(DCOS_ZK_AUTH_TYPE, DCOS_ZK_CREDS)]

DCOS_BOUNCER_LOCK_PATH='/bouncer/datastore/locking'
DCOS_BOUNCER_DATA_PATH='/cosmos/package'

print('hosts='+DCOS_ZK_HOSTS+",auth_data="+DCOS_ZK_AUTH_DATA)

zk = KazooClient(hosts=DCOS_ZK_HOSTS, auth_data=DCOS_ZK_AUTH_DATA)
zk.start()
if zk.exists(DCOS_BOUNCER_DATA_PATH):
    with zk.Lock(DCOS_BOUNCER_LOCK_PATH):
        data, stat = zk.get(DCOS_BOUNCER_DATA_PATH)
    print(data.decode())
zk.stop()
