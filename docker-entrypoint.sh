#!/bin/sh

flask db update

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"