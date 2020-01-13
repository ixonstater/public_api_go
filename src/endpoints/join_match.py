from pyramid.response import Response

class JoinMatch:
    
    def __init__(self, request):
        self.request = request

    def processRequest(self):
        return Response("j")