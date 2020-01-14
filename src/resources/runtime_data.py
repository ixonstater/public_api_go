import json
from datetime import datetime

class Matches:

    def __init__(self):
        self.matchDump = {}

    def retrieveMatchData(self, accessToken):
        pass

    def setMatchData(self, accessToken, newState):
        pass

    def addMatch(self, accessToken, newMatch):
        self.matchDump[accessToken] = newMatch

    def removeInactiveMatches(self):
        pass

    def isNotUniqueAccessToken(self, token):
        return token in self.matchDump


class Match:

    def __init__(self, gameState, blackToken):
        self.blackToken = blackToken
        self.whiteToken = None
        self.lastUpdated = datetime.now()
        self.gameState = gameState

    


class Model:
    def __init__():
        pass