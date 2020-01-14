from pyramid.response import Response

class RequestState:
    
    def __init__(self, context, request):
        self.request = request
        self.requestBody = None
        self.context = context
        self.validRequest = True

    def processRequest(self):
        self.sanitizeRequest()
        if(not self.validRequest):
            return Response('An internal error occured.')
        
        elif(not self.context.matches.newStateExists(self.requestBody['accessToken'], self.requestBody['whosTurn'])):
            return Response ('{}')

        else:

            return Response(self.context.matches.getMatchStateAsJSON(self.requestBody['accessToken']))

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if (not self.context.matches.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
        