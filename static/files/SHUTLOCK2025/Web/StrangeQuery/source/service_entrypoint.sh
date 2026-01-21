#!/bin/bash

sleep 10
flask db migrate
flask db upgrade 
waitress-serve --port 5000 --call 'best_app:create_app'

tail -f /dev/null

SQLALCHEMY_DATABASE_URI = "postgresql://cool_user:1234@db:5432/cool_db"
