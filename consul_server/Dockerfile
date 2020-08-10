FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
    bash curl nano net-tools zip unzip \
    jq dnsutils iputils-ping

RUN curl  https://releases.hashicorp.com/consul/1.8.0/consul_1.8.0_linux_amd64.zip > /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

# Consul ports
EXPOSE 8300 8301 8302 8400 8500 53

ADD consul_server.sh /opt
RUN mkdir -p /data
VOLUME /data

CMD ["bash","/opt/consul_server.sh"]
