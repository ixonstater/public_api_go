#/bin/bash

#create server code wheel
bin/python3 src/setup.py bdist_wheel

#install wheel in local venv

#start server with installed wheel
bin/mod_wsgi-express start-server ./src/wsgi_connector.py

