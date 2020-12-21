#!/bin/bash
echo "Starting my app."
cd /home/ubuntu/cafeteriaBrioche
source env/bin/activate
sudo /home/ubuntu/cafeteriaBrioche/env/bin/gunicorn --workers=20 -b 0.0.0.0:443 --certfile=server.cert --keyfile=server.key wsgi:application
