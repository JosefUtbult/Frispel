#!/bin/sh

cp -a /var/www/frispel.rocks/db.sqlite3 "/home/josef-user/db_backup/$(date -I)-db.sqlite3"
