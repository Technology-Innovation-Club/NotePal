#!/bin/bash
pip install --no-cache-dir -r requirements.txt
python manage.py migrate

if [ ! -f /.container_created ]; then
    echo "Setting up..."

    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'ticadmin')" | python manage.py shell


    touch /.container_created
fi

python manage.py runserver 0.0.0.0:9000