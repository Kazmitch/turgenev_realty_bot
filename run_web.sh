#!/bin/sh

bash -c 'pip3 install -r requirements.txt'
bash -c 'pip3 freeze'
# wait for PSQL server to start
sleep 10

# prepare init migration
bash -c "python3 django_app.py makemigrations --noinput"
# migrate db, so we have the latest db schema
bash -c "python3 django_app.py migrate"
MAIL=""
script="
from django.contrib.auth.models import User;
username = '$DJANGO_USER';
password = '$DJANGO_PASSWORD';
email = '$MAIL';
if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python3 django_app.py shell

bash -c "python3 django_app.py makemigrations"
bash -c "python3 django_app.py migrate"
#bash -c "python django_app.py collectstatic --noinput"
#bash -c "crontab /realty_tg_bot/crontab"
#bash -c "service cron restart"

bash -c "python3 django_app.py runserver 0.0.0.0:8000"
