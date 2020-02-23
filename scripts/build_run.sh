#!/bin/bash
./scripts/build.sh

#start server with installed wheel
bin/mod_wsgi-express start-server ./src/wsgi_connector.py

