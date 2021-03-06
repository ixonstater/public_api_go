from src.resources import instance
from src import config as appConfig
from wsgiref.simple_server import make_server

def main():
    inst = instance.Instance()
    app = inst.initServer()
    
    server = make_server('0.0.0.0', appConfig.PORT, app)
    server.serve_forever()

main()