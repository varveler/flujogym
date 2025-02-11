#!/bin/sh
python3 manage.py migrate --noinput
if [ ! -f "/flujogym/.fixtures-loaded" ]; then
    python3 manage.py loaddata usuarios.json rutinas.json
    touch /flujogym/.fixtures-loaded
fi
python3 manage.py collectstatic --noinput
/usr/local/bin/gunicorn flujogym.wsgi:application -w 3 -b :80 --reload --log-level debug --timeout 90