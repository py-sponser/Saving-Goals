#!/usr/bin/bash

set -e

PROJECT_BASE_PATH='/usr/local/apps/savings'

cd $PROJECT_BASE_PATH
git pull
$PROJECT_BASE_PATH/env/bin/python manage.py makemigrations
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart savings

echo "DONE! :)"
