from pyramid.paster import get_app, setup_logging

ini_path = 'src/production.ini'
application = get_app(ini_path, 'main')