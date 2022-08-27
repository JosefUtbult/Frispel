# Frispel

## Todo

* Add start page text

* Add about tab and text

* Add rules tab and content

* Make a temporary number of alowed bookings, until a specific date

* Add a form for changing password for users.

* Add an option under each user for manager to reset a users password to a static one. Make a check when users log in, if the hash is the same as the hash for the static password, and send the user directly to the change password prompt if it is.

* Make sure users cant book with the static password enabled password

* Create a log file system for prints

* Add english

## Setup

Använd guider från digitalocean. [Set up Nginx](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04) och [Set up Django with NginX](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04)

### Virtual mashine

Skapa en virtuell maskin på [DUST](https://dust.ludd.ltu.se/cloud/dashboard). Sätt OS till Ubuntu 20.04 LTS och storlek 
till Large. Döp den till _frispel-rocks_.

Assigna den statiska IPn `130.240.202.215`.

Spara undan det temporära SSH lösenordet.

### På maskinen

SSHa in med användaren frispel och det temporära lösenordet.

```
ssh frispel@130.240.202.215
```

Byt lösenord med `passwd` till det sparat i lösenordshanteraren

Installera nginx och pip

```bash 
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y nginx python3-pip python3-venv uwsgi uwsgi-plugin-python3 certbot python3-certbot-nginx python3-venv
```

### Hämta repot

* Clona repot från GIT till `home/frispel`.

```bash
git clone https://github.com/JosefUtbult/Frispel.git /home/frispel/Frispel
```

* Kopiera över *secret_key.txt*, *GoogleMail/token.pickle*, *GoogleCalendar/token.pickle* och *db.sqlite3* över ssh.

* Redigera *Frispel/settings.py*. Byt DEBUG till False

### Skapa en virtuel miljö

* Använd pythons virtuella milö generator.

```bash
cd /home/frispel/Frispel
python3 -m venv venv
source venv/bin/activate
```

### Installera requirements

* Installera requirements från *requirements.txt*

```bash
pip install -r requirements.txt 
```

### Skapa sym-links till projektmappen

* Symlinka projektmappen, *frispel_uwsgi.ini* och *frispel.rocks*

```bash
sudo ln -s /home/frispel/Frispel /var/www/frispel.rocks
sudo ln -s /home/frispel/Frispel/frispel_uwsgi.ini /etc/uwsgi/apps-enabled/
sudo ln -s /home/frispel/Frispel/setup/nginx/frispel.rocks /etc/nginx/sites-enabled/
```

### Skapa ett Origin Certificate på Cloudflare

* Logga in på Cloudflare, gå till *SSL/TLS* -> *Origin Server*

* Välj *Create Certificate*

* Använd standardinställningarna

* Kopiera *Origin Certificate* till `/etc/ssl/frispel_cert.pem` och *Private Key* till `/etc/ssl/frispel_key.pem`

### Generera Nginx config med certbot

* Använd certbot

```bash
grep -R /etc/letsencrypt/live/frispel.rocks/fullchain.pem /etc/nginx/
sudo certbot --nginx
```

* Registrera *frispel.webmaster@gmail.com* som kontaktadress.

* Godkänn avtalet, neka till att dela mailadressen.

* Välj alla aktiva HTTPS adresser igenom att trycka enter.

* Välj att all HTTP trafik ska redirectas till HTTPS.

### Omstart

* Starta om Nginx och uwsgi.

```bash
sudo systemctl restart uwsgi.service
sudo systemctl restart nginx.service
```

* Kolla status på servicerna.

```bash
sudo systemctl status uwsgi.service
sudo systemctl status nginx.service
```

* Nu bör allt funka som det ska. Se till så att mappen och alla filer i den ägs av användaren *frispel*

```bash
ll /home/frispel
```
