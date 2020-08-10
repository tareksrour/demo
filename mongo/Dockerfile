FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
    bash curl nano net-tools zip unzip \
    jq dnsutils iputils-ping

RUN apt-get install -y net-tools
# Install MongoDB
RUN apt-get install -y mongodb

# Setup Consul and Goreman
RUN mkdir -p /data/db

RUN curl  https://releases.hashicorp.com/consul/1.8.0/consul_1.8.0_linux_amd64.zip > /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

RUN mkdir -p /etc/consul.d/check_scripts

ADD mongo_primary.sh /etc/consul.d/check_scripts
RUN chmod +x /etc/consul.d/check_scripts/mongo_primary.sh
ADD mongo_primary.json /etc/consul.d/
ADD config.js /tmp/
ADD consul.sh /tmp/
ADD mongo.sh /tmp/
RUN chmod +x /tmp/consul.sh
RUN chmod +x /tmp/mongo.sh
ADD wait-for-it.sh /tmp/
RUN chmod +x /tmp/wait-for-it.sh

EXPOSE $MONGO_PORT

ENTRYPOINT ["bash","/tmp/consul.sh"]
