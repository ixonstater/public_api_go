from pyramid.response import Response

class RequestMatch:

    def __init__(self, request):
        self.request = request

    def processRequest(self):
        return Response("r")