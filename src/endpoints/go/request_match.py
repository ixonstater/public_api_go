from pyramid.response import Response
from resources.go.runtime_data import Match
import random
import string
import json
from resources.go import const

class RequestMatch:

    def __init__(self, context, request):
        self.request = request
        self.response = None
        self.context = context
        self.validRequest = True

    def processRequest(self):
        self.validateRequest()
        if(self.validRequest):
            accessToken = self.generateAccessToken()
            newMatch = Match()
            newMatch.gameState['whosTurn'] = self.requestBody['whosTurn']
            self.context.addMatch(accessToken, newMatch)
            self.response = Response(json.dumps(accessToken))

        return self.response

    def validateRequest(self):
        self.requestBody = self.request.json
        whosTurn = self.requestBody['whosTurn']
        if(whosTurn != const.BLACK and whosTurn != const.WHITE):
            self.validRequest = False
            self.response = Response(json.dumps('Invalid color submitted'))

    def generateAccessToken(self):
        notUnique = True
        while(notUnique):
            letters = string.ascii_lowercase
            letters = ''.join(random.choice(letters) for i in range(5))
            notUnique = self.context.tokenExists(letters)
        return letters