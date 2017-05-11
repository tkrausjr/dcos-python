# DCOS Python 
This repo contains scripts for working with and getting infomration from your DCOS EE Cluster.

# mesos Folder
The mesos folder contains Python scripts for interacting with Apache Mesos. To get more details look at the README in mesos folder.

# marathon Folder
The marathon folder contains a sample script that leverages the modules/marathon.py python module to interact with Marathon on DCOS.  To get more details look at the README in marathon folder.

# zookeeper Folder
The mesos folder contains Python scripts for interacting with Apache Zookeeper through Python. To get more details look at the README in zookeeper folder.

# modules Folder
The modules folder contains Python classes for DCOS ACS, Marathon, and Apache Mesos that can be imported and called from other scripts

## Requirements
These scripts have only been tested with python3.5 as of now, requests and json Standard Python modules and a mesos Python module which is included \


## Usage
1) git clone https://github.com/tkrausjr/dcos-python.git
2) cd dcos-python/marathon
3) python3 marathon_sample.py
4) cd dcos-python/mesos
5) python3 mesos_resources.py




