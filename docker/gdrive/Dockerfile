FROM ubuntu:23.04

RUN apt update -y && apt upgrade -y && apt install -y wget

COPY upload_script /bin

RUN chmod +x /bin/upload_script

RUN wget https://github.com/glotlabs/gdrive/releases/download/3.9.0/gdrive_linux-x64.tar.gz -P /root

RUN cd /bin && tar -xf /root/gdrive_linux-x64.tar.gz 

RUN chmod +x /bin/gdrive

WORKDIR /root

ENTRYPOINT upload_script
