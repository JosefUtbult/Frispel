FROM ubuntu:23.04

RUN apt update -y
RUN apt upgrade -y
Run apt install -y \
	nginx \
	python3-pip \
	python3-venv \
	uwsgi \
	uwsgi-plugin-python3 \
	certbot \
	python3-certbot-nginx \
	python3-venv

COPY requirements.txt /root/requirements.txt

COPY site /root/frispel

RUN pip install -r /root/requirements.txt --break-system-packages

WORKDIR /root/frispel

ENTRYPOINT gunicorn --bind 0.0.0.0:8000 Frispel.wsgi

