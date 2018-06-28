#!/bin/bash

source settings/deploy.conf
source settings/secrets.conf
source settings/database.conf

sudo rsync -a ./venv ${TARGET}
sudo rsync -a --exclude='VLE.db' --exclude='settings/development.py' --exclude='test/' --exclude="__pycache__" --exclude="migrations/" ./src/django ${TARGET}

sudo sed -i "s@{{DIR}}@${TARGET}/django@g" ${TARGET}/django/VLE/wsgi.py

sudo sed -i "s@{{DATABASE_TYPE}}@${DATABASE_TYPE}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_NAME}}@${DATABASE_NAME}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_USER}}@${DATABASE_USER}@g" ${TARGET}/django/VLE/settings/production.py

sudo sed -i "s@{{DATABASE_PASSWORD}}@${DATABASE_PASSWORD}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_PORT}}@${DATABASE_PORT}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{DATABASE_HOST}}@${DATABASE_HOST}@g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@{{BASELINK}}@${TYPE}://${SERVERNAME}${HOOKPOINT}@g" ${TARGET}/django/VLE/settings/production.py

sudo sed -i "s'{{SECRET_KEY}}'${SECRET_KEY}'g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s'{{LTI_SECRET}}'${LTI_SECRET}'g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s'{{LTI_KEY}}'${LTI_KEY}'g" ${TARGET}/django/VLE/settings/production.py
sudo sed -i "s@development@production@g" ${TARGET}/django/manage.py

sudo rm -rd ${TARGET}django/VLE/migrations
mkdir ${TARGET}django/VLE/migrations || sudo mkdir ${TARGET}django/VLE/migrations
touch ${TARGET}django/VLE/migrations/__init__.py || sudo touch ${TARGET}django/VLE/migrations/__init__.py

source ${TARGET}venv/bin/activate
python ${TARGET}django/manage.py makemigrations
python ${TARGET}django/manage.py migrate
python ${TARGET}django/manage.py collectstatic --noinput
python ${TARGET}django/manage.py check --deploy
deactivate

rsync -a ${TARGET}django/static ${TARGET}static
