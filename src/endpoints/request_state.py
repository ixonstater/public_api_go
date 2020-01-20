from pyramid.response import Response
import json

class RequestState:
    
    def __init__(self, context, request):
        self.request = request
        self.requestBody = None
        self.context = context
        self.validRequest = True

    def processRequest(self):
        self.sanitizeRequest()
        if(not self.validRequest):
            self.response = 'An internal error occured.'
        
        elif(not self.context.matches.newStateExists(self.requestBody['accessToken'], self.requestBody['whosTurn'])):
            self.response = '{}'

        else:
            self.response = json.dumps(self.context.matches.getMatchState(self.requestBody['accessToken']))

        return Response(json.dumps(self.response))

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if (not self.context.matches.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
        