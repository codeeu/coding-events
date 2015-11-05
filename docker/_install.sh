#!/bin/bash

apt-get -y update
apt-get -u upgrade
apt-get install -y libjpeg-dev python-dev python-setuptools supervisor ruby-sass python-geoip libmysqlclient-dev git texlive-base texlive-latex-base

easy_install pip
pip install uwsgi

cd /opt
git clone https://github.com/codeeu/coding-events.git

cd coding-events
git checkout "{{check-tag}}"

pip install -r server-requirements.txt

./manage.py collectstatic --noinput
./manage.py compress --force

cat << EOF > /opt/run
#!/bin/bash
. /opt/prepare_db_var.sh
export DATABASE_URL
supervisord -c /opt/supervisor.conf -n
EOF
chmod 754 /opt/run

echo 'DATABASE_URL="mysql://${DB_USER}:${DB_PASS}@${MYSQL_PORT_3306_TCP_ADDR}:${MYSQL_PORT_3306_TCP_PORT}/${DB_NAME}"' > /opt/prepare_db_var.sh
chmod 644 /opt/prepare_db_var.sh

cat << EOF > /opt/supervisor.conf
[supervisord]
nodaemon=true

[program:app]
priority=10
directory=/opt/coding-events
command=/usr/local/bin/uwsgi
    --http-socket 0.0.0.0:8000
    -p 4
    -b 32768
    -T
    --master
    --max-requests 5000
    --static-map /static=/opt/coding-events/staticfiles
    --module codeweekeu.wsgi:application
user=root
autostart=true
autorestart=true
EOF
