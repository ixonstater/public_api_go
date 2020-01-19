from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from endpoints.join_match import JoinMatch
from endpoints.request_match import RequestMatch
from endpoints.submit_turn import SubmitTurn
from endpoints.request_state import RequestState
from resources.runtime_data import Matches

class Instance:

    def __init__(self):
        self.server = None
        self.matches = Matches()


    def initServer(self):
        with Configurator() as config:
            config.add_route('requestMatch', '/requestMatch')
            config.add_route('joinMatch', '/joinMatch')
            config.add_route('submitTurn', '/submitTurn')
            config.add_route('requestState', '/requestState')
            config.add_static_view('/', '/home/ixonstater/code/go_client/')

            config.add_view(self.requestMatch, route_name='requestMatch')
            config.add_view(self.joinMatch, route_name='joinMatch')
            config.add_view(self.submitTurn, route_name='submitTurn')
            config.add_view(self.requestState, route_name='requestState')

            app = config.make_wsgi_app()
            
        server = make_server('0.0.0.0', 8080, app)
        self.server = server
        server.serve_forever()

    def requestMatch(self, request):
        matchRequest = RequestMatch(self, request)
        return matchRequest.processRequest()

    def joinMatch(self, request):
        matchJoin = JoinMatch(self, request)
        return matchJoin.processRequest()

    def submitTurn(self, request):
        turnSubmit = SubmitTurn(self, request)
        return turnSubmit.processRequest()

    def requestState(self, request):
        stateRequest = RequestState(self, request)
        return stateRequest.processRequest()