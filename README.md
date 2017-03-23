# dcos-python



## Background

## Usage

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