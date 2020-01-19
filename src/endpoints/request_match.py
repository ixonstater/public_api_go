from pyramid.response import Response
from resources.runtime_data import Match
import random
import string
import json
from resources import const

class RequestMatch:

    def __init__(self, context, request):
        self.request = request
        self.requestBody = None
        self.context = context
        self.validRequest = True

    def processRequest(self):
        self.sanitizeRequest()
        if(not self.validRequest):
            return Response("An internal error occured.")

        accessToken = self.generateAccessToken()
        newMatch = Match(self.requestBody['blackToken'])
        self.context.matches.addMatch(accessToken, newMatch)

        return Response(json.dumps(accessToken))

    def sanitizeRequest(self):
        self.requestBody = self.request.json

    def generateAccessToken(self):
        notUnique = True
        while(notUnique):
            letters = string.ascii_lowercase
            letters = ''.join(random.choice(letters) for i in range(5))
            notUnique = self.context.matches.tokenExists(letters)
        return letters