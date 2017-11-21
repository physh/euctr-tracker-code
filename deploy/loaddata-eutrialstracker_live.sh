#!/bin/sh

export GIT_SSH_COMMAND='ssh -i /var/www/eutrialstracker_live/ssh-keys/id_rsa_eutrialtracker_data' 

. /etc/profile.d/eutrialstracker_live.sh

cd /var/www/eutrialstracker_live/euctr-tracker-data
git pull -q
chown -R www-data:www-data .

cd /var/www/eutrialstracker_live/
. venv/bin/activate
cd euctr-tracker-code/euctr
./manage.py get_trials_from_db
./manage.py update_trials_json

cd /var/www/eutrialstracker_live/euctr-tracker-data
git commit -qa --author="Cron <>" --message="Automatic commit from eutrialstracker-live-cron"
git push -q
chown -R www-data:www-data .