
# Postgresql HA cluster in docker using Patroni and Consul.

This is a minimalistic demo application showing HA Postgresql cluster managed by Patroni and Consul with no extra load balancers.
The entire setup runs in `docker-compose` and requires `make` utility for helper commands.

For Postgresql and application containers the vanilla `ubuntu:20.04` image is used and for Consul servers the official `consul:1.9.3` image.

Patroni nodes run 2 services under supervisor: patroni and consul in agent mode.

Consul nodes run consul service in server mode.

Application nodes run 3 services under supervisor: consul in agent mode, dnsmasq and application itself.

Application connects to a current Postgresql master node and reports to the log its IP address.


```
                 ┌───dns:8600──┐                    ┌─────────────┐                            
                 │             │                    │             │                            
                 │             │                    │             │                            
       ┌──────────────────┐    │          ┌──────────────────┐    │                            
       │                  │    │          │                  │    │                            
       │  application01   ├─┐  │  ┌───────│  application02   ├─┐  │                            
       │                  │ │  │  │       │                  │ │  │                            
       └───┬──────────────┘ │◀─┘  │       └───┬──────────────┘ │◀─┘                            
       │   │    consul-agent│     │           │    consul-agent│                               
       │   └────────────────┘     │           └────────────────┘                               
       │            │             │                    │                                       
       │            │             │       ┌────────────┘                                       
       │            │             │       │                                                    
       │            │             │       ▼                                                    
       │            │             │.─────────────.                                             
       │            │           ,─'               '─.                                          
 postgres:5432      └─────────▶(      consul01       )                                         
       │                        `─┬.             _.─'──.                                       
       │                          │ `───────────'       '─.                                    
       │                          │  (      consul02       )◀───────────rpc:8300──────────────┐
       │                          │   `──.             _.─'──.                                │
       │                          │       `───────────'       '─.                             │
       │                          │ ┌─────▶(      consul03       )◀─┐                         │
       │                          │ │       `──.             _.─'   │                         │
       │                          │ │           `───────────'       │                         │
       │                          │ │                               │                         │
       ▼                          │ │                               │                         │
       ╔═══════════════════╗      │ │    ╔═══════════════════╗      │   ╔═══════════════════╗ │
       ║ PG                ║      │ │    ║ PG                ║      │   ║ PG                ║ │
       ║                   ║      │ │    ║                   ║      │   ║                   ║ │
    ┌──║     patroni01     ║◀─────┘ │ ┌──║     patroni02     ║      │┌──║     patroni03     ║ │
    │  ║                   ╠─┐      │ │  ║                   ╠─┐    ││  ║                   ╠─┐
    │  ║         [leader]  ║ │      │ │  ║         [follower]║ │    ││  ║         [follower]║ │
    │  ╚════╦══════════════╝ │──────┘ │  ╚════╦══════════════╝ │────┘│  ╚════╦══════════════╝ │
    │       │    consul-agent│        │       │    consul-agent│     │       │    consul-agent│
    │       └────────────────┘        │       └────────────────┘     │       └────────────────┘
    │                ▲                │                ▲             │                ▲        
    │   http:8500    │                │                │             │                │        
    └────────────────┘                └────────────────┘             └────────────────┘        
```

## Usage

### `make build`

```
Pull and build container images. This make take some time when running for first time.
...
```

### `make start`

```
Start cluster
Creating consul02      ... done
Creating consul01      ... done
Creating consul03      ... done
Creating patroni02     ... done
Creating application01 ... done
Creating patroni03     ... done
Creating patroni01     ... done
Creating application02 ... done
```


### `make status`

```
============================== Docker status ==============================
    Name                   Command               State                                                         Ports
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
application01   /usr/bin/entrypoint.sh           Up
application02   /usr/bin/entrypoint.sh           Up
consul01        docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 0.0.0.0:8500->8500/tcp, 0.0.0.0:8600->8600/tcp,
                                                         0.0.0.0:8600->8600/udp
consul02        docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 8500/tcp, 8600/tcp, 8600/udp
consul03        docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 8500/tcp, 8600/tcp, 8600/udp
patroni01       /usr/bin/entrypoint.sh           Up
patroni02       /usr/bin/entrypoint.sh           Up
patroni03       /usr/bin/entrypoint.sh           Up

============================== Consul status ==============================
Node           Address          Status  Type    Build  Protocol  DC   Segment
consul01       172.22.0.4:8301  alive   server  1.9.3  2         dc1  <all>
consul02       172.22.0.2:8301  alive   server  1.9.3  2         dc1  <all>
consul03       172.22.0.3:8301  alive   server  1.9.3  2         dc1  <all>
application01  172.22.0.7:8301  alive   client  1.9.3  2         dc1  <default>
application02  172.22.0.6:8301  alive   client  1.9.3  2         dc1  <default>
patroni01      172.22.0.9:8301  alive   client  1.9.3  2         dc1  <default>
patroni02      172.22.0.5:8301  alive   client  1.9.3  2         dc1  <default>
patroni03      172.22.0.8:8301  alive   client  1.9.3  2         dc1  <default>

============================== Patroni status =============================
+ Cluster: pglab (6952903817239490606) -----+----+-----------+
| Member    | Host      | Role    | State   | TL | Lag in MB |
+-----------+-----------+---------+---------+----+-----------+
| patroni01 | patroni01 | Leader  | running |  1 |           |
| patroni02 | patroni02 | Replica | running |  1 |         0 |
| patroni03 | patroni03 | Replica | running |  1 |         0 |
+-----------+-----------+---------+---------+----+-----------+
```

### `make stop`

```
Stop cluster
Stopping application01 ... done
Stopping application02 ... done
Stopping patroni01     ... done
Stopping patroni03     ... done
Stopping patroni02     ... done
Stopping consul01      ... done
Stopping consul03      ... done
Stopping consul02      ... done
```

### `make destroy`

```
Force destroy cluster
Stopping application01 ... done
Stopping application02 ... done
Stopping patroni01     ... done
Stopping patroni03     ... done
Stopping patroni02     ... done
Stopping consul03      ... done
Stopping consul02      ... done
Stopping consul01      ... done
Removing application01 ... done
Removing application02 ... done
Removing patroni01     ... done
Removing patroni03     ... done
Removing patroni02     ... done
Removing consul03      ... done
Removing consul02      ... done
Removing consul01      ... done
Removing network postgresql-consul-demo_pglab
```

### `make recreate`

```
Destroy and recreate cluster
Stopping application02 ... done
Stopping application01 ... done
Stopping patroni01     ... done
Stopping patroni03     ... done
Stopping consul03      ... done
Stopping patroni02     ... done
Stopping consul02      ... done
Stopping consul01      ... done
Going to remove application02, application01, patroni01, patroni03, consul03, patroni02, consul02, consul01
Removing application02 ... done
Removing application01 ... done
Removing patroni01     ... done
Removing patroni03     ... done
Removing consul03      ... done
Removing patroni02     ... done
Removing consul02      ... done
Removing consul01      ... done
Creating consul02      ... done
Creating consul01      ... done
Creating patroni02     ... done
Creating application01 ... done
Creating consul03      ... done
Creating application02 ... done
Creating patroni03     ... done
Creating patroni01     ... done
```

### `make switchover`

```
Force patroni switchover to another node
Current cluster topology
+ Cluster: pglab (6952826428965204016) -----+----+-----------+
| Member    | Host      | Role    | State   | TL | Lag in MB |
+-----------+-----------+---------+---------+----+-----------+
| patroni01 | patroni01 | Replica | running |  3 |         0 |
| patroni02 | patroni02 | Leader  | running |  3 |           |
| patroni03 | patroni03 | Replica | running |  3 |         0 |
+-----------+-----------+---------+---------+----+-----------+
2021-04-19 11:27:44.11792 Successfully switched over to "patroni01"
+ Cluster: pglab (6952826428965204016) -----+----+-----------+
| Member    | Host      | Role    | State   | TL | Lag in MB |
+-----------+-----------+---------+---------+----+-----------+
| patroni01 | patroni01 | Leader  | running |  3 |           |
| patroni02 | patroni02 | Replica | stopped |    |   unknown |
| patroni03 | patroni03 | Replica | running |  3 |         0 |
+-----------+-----------+---------+---------+----+-----------+
```

### `make applogs`

```
Attaching to application02, application01
application01    | 2021-04-19 16:42:32,564 CRIT Supervisor is running as root.  Privileges were not dropped because no user is specified in the config file.  If you intend to run as root, you can set user=root in the config file to avoid this message.
application01    | 2021-04-19 16:42:32,564 INFO Included extra file "/etc/supervisor/conf.d/application.conf" during parsing
application01    | 2021-04-19 16:42:32,564 INFO Included extra file "/etc/supervisor/conf.d/consul.conf" during parsing
application01    | 2021-04-19 16:42:32,572 INFO RPC interface 'supervisor' initialized
application01    | 2021-04-19 16:42:32,573 CRIT Server 'unix_http_server' running without any HTTP authentication checking
application01    | 2021-04-19 16:42:32,573 INFO supervisord started with pid 8
application01    | 2021-04-19 16:42:33,578 INFO spawned: 'application' with pid 10
application01    | 2021-04-19 16:42:33,583 INFO spawned: 'consul' with pid 11
application01    | 2021-04-19 16:42:33,587 INFO spawned: 'dnsmasq' with pid 12
application01    | 2021-04-19 16:42:34,114 INFO Starting.
application01    | 2021-04-19 16:42:34,131 INFO Connecting.
application01    | 2021-04-19 16:42:34,333 ERROR could not translate host name "master.pglab.service.consul" to address: Name or service not known
application01    |
application01    | 2021-04-19 16:42:35,336 INFO success: application entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
application01    | 2021-04-19 16:42:35,336 INFO success: consul entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
application01    | 2021-04-19 16:42:35,336 INFO success: dnsmasq entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
application01    | 2021-04-19 16:42:36,337 INFO Connecting.
application01    | 2021-04-19 16:42:38,768 ERROR could not translate host name "master.pglab.service.consul" to address: Name or service not known
application01    |
application01    | 2021-04-19 16:42:40,771 INFO Connecting.
application01    | 2021-04-19 16:42:40,775 ERROR could not translate host name "master.pglab.service.consul" to address: Name or service not known
application01    |
application01    | 2021-04-19 16:42:42,778 INFO Connecting.
application01    | 2021-04-19 16:42:42,801 INFO I'm connected to 172.24.0.5
application01    | 2021-04-19 16:42:43,804 INFO I'm connected to 172.24.0.5
application01    | 2021-04-19 16:42:44,805 INFO I'm connected to 172.24.0.5
...
```
