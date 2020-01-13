from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from endpoints.join_match import JoinMatch
from endpoints.request_match import RequestMatch
from endpoints.submit_turn import SubmitTurn

class Instance:

    def __init__(self):
        self.server = None


    def initServer(self):
        with Configurator() as config:
            config.add_route('requestMatch', '/requestMatch')
            config.add_route('joinMatch', '/joinMatch')
            config.add_route('submitTurn', '/submitTurn')

            config.add_view(self.requestMatch, route_name='requestMatch')
            config.add_view(self.joinMatch, route_name='joinMatch')
            config.add_view(self.submitTurn, route_name='submitTurn')

            app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 8080, app)
        self.server = server
        server.serve_forever()

    def requestMatch(self, request):
        matchRequest = RequestMatch(request)
        return matchRequest.processRequest()

    def joinMatch(self, request):
        matchJoin = JoinMatch(request)
        return matchJoin.processRequest()

    def submitTurn(self, request):
        turnSubmit = SubmitTurn(request)
        return turnSubmit.processRequest()