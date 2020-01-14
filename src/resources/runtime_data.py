import json
from datetime import datetime

class Matches:

    def __init__(self):
        self.matchDump = {}

    def setMatchState(self, accessToken, newState):
        self.matchDump[accessToken].gameState = newState

    def getMatchState(self, accessToken):
        return self.matchDump[accessToken].gameState

    def getMatchStateAsJSON(self, accessToken):
        return json.dumps(self.matchDump[accessToken].gameState)

    def newStateExists(self, accessToken, whosTurn):
        return self.matchDump[accessToken].gameState['whosTurn'] != whosTurn

    def addMatch(self, accessToken, newMatch):
        self.matchDump[accessToken] = newMatch
    
    def joinMatch(self, accessToken, whiteToken):
        self.matchDump[accessToken].whiteToken = whiteToken

    def tokenExists(self, token):
        return token in self.matchDump

    def removeInactiveMatches(self):
        pass


class Match:

    def __init__(self, gameState, blackToken):
        self.blackToken = blackToken
        self.whiteToken = None
        self.lastUpdated = datetime.now()
        self.gameState = gameState

    


class Model:
    def __init__():
        pass