FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt -y install lsb-release sudo vim python3-pip libpq-dev supervisor wget unzip gettext-base dnsmasq iputils-ping dnsutils pgbouncer
RUN pip3 install psycopg2
RUN useradd -ms /bin/bash pgbouncer
RUN mkdir /var/log/pgbouncer
RUN chown pgbouncer:pgbouncer /etc/pgbouncer
RUN chown pgbouncer:pgbouncer /var/log/pgbouncer

# Install consul
RUN wget --quiet https://releases.hashicorp.com/consul/1.9.3/consul_1.9.3_linux_amd64.zip
RUN unzip consul_1.9.3_linux_amd64.zip && mv consul /usr/local/bin/ && rm consul_1.9.3_linux_amd64.zip
RUN mkdir -p /etc/consul/certs && mkdir -p /consul/data

# postgresql client
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list
RUN apt update
RUN apt -y install postgresql-client-13
#

COPY ./entrypoint.sh /usr/bin/entrypoint.sh

CMD ["/usr/bin/entrypoint.sh"]
