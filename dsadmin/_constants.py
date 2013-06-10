# replicatype @see https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Directory_Server/8.1/html/Administration_Guide/Managing_Replication-Configuring-Replication-cmd.html
# 2 for consumers and hubs (read-only replicas)
# 3 for both single and multi-master suppliers (read-write replicas)
# TODO: let's find a way to be consistent - eg. using bitwise operator
(MASTER_TYPE,
 HUB_TYPE,
 LEAF_TYPE) = range(3)

REPLICA_RDONLY_TYPE = 2  # CONSUMER and HUB
REPLICA_WRONLY_TYPE = 1  # SINGLE and MULTI MASTER
REPLICA_RDWR_TYPE = REPLICA_RDONLY_TYPE | REPLICA_WRONLY_TYPE


CFGSUFFIX = "o=NetscapeRoot"
DEFAULT_USER = "nobody"

# Some DN constants
DN_DM = "cn=Directory Manager"
DN_CONFIG = "cn=config"
DN_LDBM = "cn=ldbm database,cn=plugins,cn=config"
DN_MAPPING_TREE = "cn=mapping tree,cn=config"
DN_CHAIN = "cn=chaining database,cn=plugins,cn=config"

#
# constants
#
DEFAULT_USER = "nobody"
