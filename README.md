
# Postgresql HA cluster in docker using Patroni and Consul.

For Postgresql the vanilla Ubuntu:20.04 image used with installed Postgresql 13, Patroni and Consul agents.

For Consul servers the official Consul:1.9.3 image used.

### `make build`

```
Build patroni docker container image
```

### `make start`

```
Start cluster
Creating consul01  ... done
Creating patroni03 ... done
Creating consul02  ... done
Creating patroni01 ... done
Creating patroni02 ... done
Creating consul03  ... done
```


### `make status`

```
------------------------------ Docker status ------------------------------
  Name                 Command               State                                                           Ports
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
consul01    docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 0.0.0.0:8500->8500/tcp, 0.0.0.0:8600->8600/tcp,
                                                     0.0.0.0:8600->8600/udp
consul02    docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 8500/tcp, 8600/tcp, 8600/udp
consul03    docker-entrypoint.sh agent ...   Up      8300/tcp, 8301/tcp, 8301/udp, 8302/tcp, 8302/udp, 8500/tcp, 8600/tcp, 8600/udp
patroni01   /usr/bin/entrypoint.sh           Up
patroni02   /usr/bin/entrypoint.sh           Up
patroni03   /usr/bin/entrypoint.sh           Up

------------------------------ Consul status ------------------------------
Node       Address          Status  Type    Build  Protocol  DC   Segment
consul01   172.22.0.2:8301  alive   server  1.9.3  2         dc1  <all>
consul02   172.22.0.3:8301  alive   server  1.9.3  2         dc1  <all>
consul03   172.22.0.4:8301  alive   server  1.9.3  2         dc1  <all>
patroni01  172.22.0.5:8301  alive   client  1.9.3  2         dc1  <default>
patroni02  172.22.0.7:8301  alive   client  1.9.3  2         dc1  <default>
patroni03  172.22.0.6:8301  alive   client  1.9.3  2         dc1  <default>

------------------------------ Patroni status -----------------------------
+ Cluster: pglab (6951697924355059797) -----+----+-----------+
| Member    | Host      | Role    | State   | TL | Lag in MB |
+-----------+-----------+---------+---------+----+-----------+
| patroni01 | patroni01 | Leader  | running |  1 |           |
| patroni02 | patroni02 | Replica | running |  1 |         0 |
| patroni03 | patroni03 | Replica | running |  1 |         0 |
+-----------+-----------+---------+---------+----+-----------+
```

### `make destory`

```
Destroy cluster
Stopping patroni01 ... done
Stopping patroni03 ... done
Stopping patroni02 ... done
Stopping consul03  ... done
Stopping consul02  ... done
Stopping consul01  ... done
Going to remove patroni01, patroni03, patroni02, consul03, consul02, consul01
Removing patroni01 ... done
Removing patroni03 ... done
Removing patroni02 ... done
Removing consul03  ... done
Removing consul02  ... done
Removing consul01  ... done
```

### `make recreate`

```
Destroy and recreate cluster
Stopping patroni01 ... done
Stopping patroni03 ... done
Stopping patroni02 ... done
Stopping consul03  ... done
Stopping consul01  ... done
Stopping consul02  ... done
Going to remove patroni01, patroni03, patroni02, consul03, consul01, consul02
Removing patroni01 ... done
Removing patroni03 ... done
Removing patroni02 ... done
Removing consul03  ... done
Removing consul01  ... done
Removing consul02  ... done
Creating consul03  ... done
Creating consul02  ... done
Creating patroni02 ... done
Creating patroni03 ... done
Creating patroni01 ... done
Creating consul01  ... done
```
