FROM ubuntu:24.04

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y \
	nginx \
	python3-pip \
	python3-venv \
	uwsgi \
	uwsgi-plugin-python3 \
	certbot \
	python3-certbot-nginx \
	python3-venv


WORKDIR /root
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /bin
COPY run_server .
RUN chmod +x run_server

WORKDIR /root/frispel/site
ENTRYPOINT /bin/run_server
