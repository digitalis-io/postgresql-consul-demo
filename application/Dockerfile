FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt -y install vim python3-pip libpq-dev supervisor wget unzip gettext-base dnsmasq iputils-ping dnsutils
RUN pip3 install psycopg2

# Install consul
RUN wget --quiet https://releases.hashicorp.com/consul/1.9.3/consul_1.9.3_linux_amd64.zip
RUN unzip consul_1.9.3_linux_amd64.zip && mv consul /usr/local/bin/ && rm consul_1.9.3_linux_amd64.zip
RUN mkdir -p /etc/consul/certs && mkdir -p /consul/data

COPY ./entrypoint.sh /usr/bin/entrypoint.sh

CMD ["/usr/bin/entrypoint.sh"]
