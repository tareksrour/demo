FROM ubuntu

RUN apt-get update && \
    apt-get install -y \
    bash curl nano net-tools zip unzip \
    jq dnsutils iputils-ping


RUN curl  https://releases.hashicorp.com/consul/1.8.0/consul_1.8.0_linux_amd64.zip > /tmp/consul.zip
RUN cd /bin && unzip /tmp/consul.zip && chmod +x /bin/consul && rm /tmp/consul.zip

RUN apt-get install python3 python3-pip -y
RUN pip3 install flask pymongo watchdog
RUN mkdir /tmp/watched

ADD web.json /etc/consul.d/
ADD app.py /tmp/app.py
ADD start.sh /tmp/start.sh
RUN chmod +x /tmp/start.sh

ENTRYPOINT ["bash","/tmp/start.sh"]
