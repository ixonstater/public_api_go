from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

class Instance:

    def __init__(self):
        self.server = 0


    def initServer(self):
        with Configurator() as config:
            config.add_route('gostate', '/gostate')
            config.add_view(self.goState, route_name='gostate')
            app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 6543, app)
        server.serve_forever()

    def goState(self, request):
        return Response("hello world")