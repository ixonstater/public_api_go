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
            self.response = Response(json.dumps('An internal error occured.'))

        elif(not 'whosTurn' in self.requestBody):
            self.response = Response(json.dumps(self.context.getMatchState(self.requestBody['accessToken'])))
        
        elif(not self.context.newStateExists(self.requestBody['accessToken'], self.requestBody['whosTurn'])):
            self.response = Response(json.dumps('{}'))

        else:
            self.response = Response(json.dumps(self.context.getMatchState(self.requestBody['accessToken'])))

        return self.response

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if (not self.context.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
        