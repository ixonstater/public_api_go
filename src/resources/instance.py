from pyramid.config import Configurator
from pyramid.response import Response

from src import config as appConfig
from src.endpoints.go.request_match import RequestMatch
from src.endpoints.go.submit_turn import SubmitTurn
from src.endpoints.go.request_state import RequestState
from src.resources.go.runtime_data import Matches

class Instance:

    def __init__(self):
        self.server = None
        self.matches = Matches()


    def initServer(self):
        with Configurator() as config:
            config.add_route('requestMatch', '/requestMatch')
            config.add_route('submitTurn', '/submitTurn')
            config.add_route('requestState', '/requestState')
            config.add_static_view('/', appConfig.web_root)

            config.add_view(self.requestMatch, route_name='requestMatch')
            config.add_view(self.submitTurn, route_name='submitTurn')
            config.add_view(self.requestState, route_name='requestState')

            return config.make_wsgi_app()

    def requestMatch(self, request):
        matchRequest = RequestMatch(self.matches, request)
        return matchRequest.processRequest()

    def submitTurn(self, request):
        turnSubmit = SubmitTurn(self.matches, request)
        return turnSubmit.processRequest()

    def requestState(self, request):
        stateRequest = RequestState(self.matches, request)
        return stateRequest.processRequest()
