from pyramid.paster import get_app, setup_logging

ini_path = '/home/ixonstater/code/public_api_go/src/production.ini'
application = get_app(ini_path, 'main')