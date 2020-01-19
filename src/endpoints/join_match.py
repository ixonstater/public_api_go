from pyramid.response import Response
import json

class JoinMatch:
    
    def __init__(self, context, request):
        self.request = request
        self.requestBody = None
        self.context = context
        self.validRequest = True
        self.response = None

    def processRequest(self):
        self.sanitizeRequest()
        if (not self.validRequest):
            self.response = Response("An internal error occured.")

        self.context.matches.joinMatch(self.requestBody['accessToken'], self.requestBody['whiteToken'])
        self.response = self.requestBody['accessToken']
    
        return Response(json.dumps(self.response))

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if(not self.context.matches.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
        