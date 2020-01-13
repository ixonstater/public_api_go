from pyramid.response import Response

class SubmitTurn:

    def __init__(self, request):
        self.request = request

    def processRequest(self):
        return Response("s")