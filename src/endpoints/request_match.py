from pyramid.response import Response
from resources.runtime_data import Match
import random
import string
import json
from resources import const

class RequestMatch:

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def processRequest(self):
        
        accessToken = self.generateAccessToken()
        newMatch = Match()
        self.context.matches.addMatch(accessToken, newMatch)

        return Response(json.dumps(accessToken))

    def generateAccessToken(self):
        notUnique = True
        while(notUnique):
            letters = string.ascii_lowercase
            letters = ''.join(random.choice(letters) for i in range(5))
            notUnique = self.context.matches.tokenExists(letters)
        return letters