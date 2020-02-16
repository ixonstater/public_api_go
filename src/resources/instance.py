from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

from endpoints.request_match import RequestMatch
from endpoints.submit_turn import SubmitTurn
from endpoints.request_state import RequestState
from resources.runtime_data import Matches
from resources import const
from resources import config as appConfig

class Instance:

    def __init__(self):
        self.server = None
        self.matches = Matches()


    def initServer(self):
        with Configurator() as config:
            config.add_route('requestMatch', '/requestMatch')
            config.add_route('submitTurn', '/submitTurn')
            config.add_route('requestState', '/requestState')
            config.add_static_view('/', const.WEBSITE_PATH)

            config.add_view(self.requestMatch, route_name='requestMatch')
            config.add_view(self.submitTurn, route_name='submitTurn')
            config.add_view(self.requestState, route_name='requestState')

            app = config.make_wsgi_app()
            
        server = make_server('0.0.0.0', appConfig.PORT, app)
        self.server = server
        server.serve_forever()

    def requestMatch(self, request):
        matchRequest = RequestMatch(self, request)
        return matchRequest.processRequest()

    def submitTurn(self, request):
        turnSubmit = SubmitTurn(self, request)
        return turnSubmit.processRequest()

    def requestState(self, request):
        stateRequest = RequestState(self, request)
        return stateRequest.processRequest()
