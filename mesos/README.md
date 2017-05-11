# mesos_resources.py
This script makes API calls to Mesos to obtain the Mesos Reservations, Registered Roles, Quotas, and Allocation \
for an entire cluster and then organizes this data by Cluster, Agents, and finally by Mesos Roles.

## Requirements
The script has only been tested with python2 as of now, requests and json Standard Pythong modules and a mesos Python module which is included \
in the REPO. It should work fine with Python3 with some cosmetic fixes.

## Usage
1) Update the "dcos_master", "userid", and "password" variables in the script for your DCOS cluster.
2) /usr/bin/python mesos_resources.py
3) Interpret Output - See below

## Interpretation

Data comes from the following API's

CLUSTER - LEVEL
Cluster Utilization (totals and Used) is available at /mesos/metrics/snapshot
 - This is a total an aggregate (Across all cluster nodes including static roles like slave_public)
 - This is combination of Mesos ALLOCATION which includes RESERVATIONS as well.



AGENT - LEVEL
CONFIGURED RESOURCES  /mesos/slaves
  "slaves":
   for each slave "configured_resources"
   resources:
        {
        disk:
        mem:
        gpus:
        cpus:
        ports:
        },

RESERVED RESOURCES  /mesos/slaves
  "slaves":
   for each slave   "reserved_resources_full"
        for each  role
           resources:
                {
                disk:
                mem:
                gpus:
                cpus:
                ports:
                },

USED RESOURCES   /mesos/slaves   (This is combination of Mesos ALLOCATION which includes RESERVATIONS)
  "slaves":
   for each slave "used_resources"
   resources:
        {
        disk:
        mem:
        gpus:
        cpus:
        ports:
        },

FREE RESOURCES   /mesos/slaves   (This needs to be calculated)  Outstanding
  "slaves":
   for each slave "resources" and "used_resources"
        for each "resource" (cpu,disk, mem)
            free_resource = resource.mem - used_resources.mem

## Sample Output

[a_ansible@d-2d10-u02 operations]$ /usr/bin/python mesos_resources.py
DCOS Token Received
-----------------------------
DEBUG - RAW Mesos stats =

=======================================================

DCOS Cluster MESOS ROLES Information
     Roles are as follows :

         *
         arangodb3
         cassandra-role
         confluent-kafka-role
         dev-1-gcp-test-account-heidi-test-1-role
         dev-1-gcp-test-account-kafka-20170418120736250-role
         dev-2-gcp-test-account-adamtestkafka2-role
         dev-2-gcp-test-account-kafka-20170417173032462-role
         dev-user-marathon-role
         eng-2-gcp-test-account-kafka-20170417173038127-role
         eng-user-marathon-role
         kafka-role
         prod-user-marathon-role
         slave_public
         test-1-gcp-test-account-kafka-20170417172747207-role
         test-2-gcp-test-account-kafka-20170417173044935-role
         test-user-marathon-role

=======================================================
TOTAL RESOURCES SUMMARY

=======================================================
MESOS Metrics Snapshot
MEMORY
    DCOS Mesos mem_total Configured = 7205548 MB
    DCOS Mesos mem_used = 376266.0 MB
    DCOS Mesos mem_percent = 5.22 %
CPU
    DCOS Mesos cpu_total Configured = 896 Cores
    DCOS Mesos cpu_used = 238.03 Cores
    DCOS Mesos cpu_percent = 26.57 %
DISK
    DCOS Mesos disk_total Configured = 48032474 MB
    DCOS Mesos disk_used = 997268 MB
    DCOS Mesos disk_percent = 2.08 %
FRAMEWORKS
    DCOS Mesos Connected Frameworks = 76
    DCOS Mesos Active Frameworks = 76

=======================================================
AGENTS
    DCOS Mesos Active Agents = 14
    DCOS Mesos Connected Agents = 14

=======================================================

QUOTAS Information by Role is as follows:

Quota have not been set

=======================================================
MESOS AGENTS Information
Found Mesos Agents

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S29    Hostname: 169.127.42.18
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 3.0
  Reserved DISK = 16387.0
  Reserved MEM = 2051.0
-----------------------------
Mesos Role:   cassandra-role
  Reserved CPUS = 1.5
  Reserved DISK = 10241.5
  Reserved MEM = 257.0
-----------------------------
Mesos Role:   arangodb3
  Reserved CPUS = 1.0
  Reserved DISK = 4097.0
  Reserved MEM = 4096.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S20    Hostname: 169.127.41.145
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 1.0
  Reserved DISK = 16385.0
  Reserved MEM = 2049.0
-----------------------------
Mesos Role:   dev-2-gcp-test-account-adamtestkafka2-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S28    Hostname: 169.127.41.210
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 6.0
  Reserved DISK = 16390.0
  Reserved MEM = 2054.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S22    Hostname: 169.127.41.144
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-1-gcp-test-account-adamtestkafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   arangodb3
  Reserved CPUS = 0.25
  Reserved DISK = 2048.25
  Reserved MEM = 2048.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S27    Hostname: 169.127.42.17
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-1-gcp-test-account-heidi-test-1-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   confluent-kafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   arangodb3
  Reserved CPUS = 0.25
  Reserved DISK = 2048.25
  Reserved MEM = 2048.0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 1.0
  Reserved DISK = 16385.0
  Reserved MEM = 2049.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S21    Hostname: 169.127.41.82
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 1.0
  Reserved DISK = 16385.0
  Reserved MEM = 2049.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S15    Hostname: 169.127.41.16
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-1-gcp-test-account-heidi-test-1-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   arangodb3
  Reserved CPUS = 1.0
  Reserved DISK = 4097.0
  Reserved MEM = 4096.0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 6.0
  Reserved DISK = 16390.0
  Reserved MEM = 2054.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S26    Hostname: 169.127.42.16
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 3.0
  Reserved DISK = 16387.0
  Reserved MEM = 2051.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S18    Hostname: 169.127.41.18
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 3.0
  Reserved DISK = 16387.0
  Reserved MEM = 2051.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S30    Hostname: 169.127.41.81
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   kafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 1000.0
  Reserved MEM = 513.5
-----------------------------
Mesos Role:   dev-1-gcp-test-account-adamtestkafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2304.5

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S25    Hostname: 169.127.41.209
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   confluent-kafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S19    Hostname: 169.127.41.80
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 1.0
  Reserved DISK = 16385.0
  Reserved MEM = 2049.0

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S24    Hostname: 169.127.41.208
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   dev-user-marathon-role
  Reserved CPUS = 2.0
  Reserved DISK = 16386.0
  Reserved MEM = 2049.0
-----------------------------
Mesos Role:   cassandra-role
  Reserved CPUS = 1.5
  Reserved DISK = 10241.5
  Reserved MEM = 257.0
-----------------------------
Mesos Role:   dev-2-gcp-test-account-adamtestkafka2-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5

-----------------------------------------------------------------------------------------------------
Agent ID: f08078b0-d35f-4e1b-a6d0-3bb53cdc5aff-S17    Hostname: 169.127.41.17
 Configured CPU = 64
 Configured MEM = 514682
 Configured DISK = 3430891
 Configured GPUs = 0
-----------------------------
Mesos Role:   confluent-kafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   dev-1-gcp-test-account-adamtestkafka-role
  Reserved CPUS = 1.5
  Reserved DISK = 5001.5
  Reserved MEM = 2305.5
-----------------------------
Mesos Role:   arangodb3
  Reserved CPUS = 0.25
  Reserved DISK = 2048.25
  Reserved MEM = 2048.0
-----------------------------
Mesos Role:   cassandra-role
  Reserved CPUS = 1.5
  Reserved DISK = 10241.5
  Reserved MEM = 257.0

=======================================================

RESERVATIONS Information is as follows :
Breakup by Role -

   mem-confluent-kafka-role - 6916.5
   mem-cassandra-role - 771.0
   cpus-kafka-role - 1.5
   disk-cassandra-role - 30724.5
   cpus-cassandra-role - 4.5
   mem-dev-1-gcp-test-account-heidi-test-1-role - 4611.0
   mem-dev-1-gcp-test-account-adamtestkafka-role - 6915.5
   disk-arangodb3 - 14338.75
   disk-dev-1-gcp-test-account-heidi-test-1-role - 10003.0
   cpus-dev-user-marathon-role - 27.0
   disk-dev-2-gcp-test-account-adamtestkafka2-role - 10003.0
   cpus-dev-1-gcp-test-account-adamtestkafka-role - 4.5
   disk-dev-user-marathon-role - 163867.0
   mem-kafka-role - 513.5
   cpus-confluent-kafka-role - 4.5
   disk-dev-1-gcp-test-account-adamtestkafka-role - 15004.5
   cpus-arangodb3 - 2.75
   cpus-dev-2-gcp-test-account-adamtestkafka2-role - 3.0
   mem-dev-2-gcp-test-account-adamtestkafka2-role - 4611.0
   disk-kafka-role - 1000.0
   mem-dev-user-marathon-role - 20506.0
   cpus-dev-1-gcp-test-account-heidi-test-1-role - 3.0
   disk-confluent-kafka-role - 15004.5
   mem-arangodb3 - 14336.0

Total Reservations by Resource

   Reserved Mem is :59180.5
   Reserved CPU is :50.75
   Reserved Disk is :259945.25

=======================================================

