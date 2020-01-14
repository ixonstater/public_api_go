from pyramid.response import Response

class JoinMatch:
    
    def __init__(self, context, request):
        self.request = request
        self.requestBody = None
        self.context = context
        self.validRequest = True

    def processRequest(self):
        self.sanitizeRequest()
        if (not self.validRequest):
            return Response("An internal error occured.")

        self.context.matches.joinMatch(self.requestBody['accessToken'], self.requestBody['whiteToken'])
        return Response(self.requestBody['accessToken'])

    def sanitizeRequest(self):
        self.requestBody = self.request.json
        if(not self.context.matches.tokenExists(self.requestBody['accessToken'])):
            self.validRequest = False
        