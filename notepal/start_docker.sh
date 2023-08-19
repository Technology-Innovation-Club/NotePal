#!/bin/bash
python manage.py migrate


docker run -d -p 9000:9000 -p 5434:5432 --env-file=.env notepal_web
# Set your OpenAI API key here

if [ ! -f /.container_created ]; then
    echo "Setting up..."

    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'ticadmin')" | python manage.py shell


    touch /.container_created
fi

python manage.py runserver 0.0.0.0:9000