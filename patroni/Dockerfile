FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt -y install sudo vim bash-completion wget gnupg2 lsb-core unzip net-tools supervisor curl 

# Install postgresql and patroni
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >  /etc/apt/sources.list.d/pgdg.list
RUN apt update && apt -y install postgresql-13 postgresql-client-13 patroni python3-consul
RUN mkdir /pg_data && chown postgres:postgres /pg_data

# Install consul
RUN wget --quiet https://releases.hashicorp.com/consul/1.9.3/consul_1.9.3_linux_amd64.zip
RUN unzip consul_1.9.3_linux_amd64.zip && mv consul /usr/local/bin/ && rm consul_1.9.3_linux_amd64.zip
RUN mkdir -p /etc/consul/certs && mkdir -p /consul/data

COPY ./bootstrap-patroni.sh /usr/bin/bootstrap-patroni.sh
COPY ./entrypoint.sh /usr/bin/entrypoint.sh

CMD ["/usr/bin/entrypoint.sh"]
