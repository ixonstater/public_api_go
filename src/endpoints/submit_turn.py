from pyramid.response import Response

class SubmitTurn:

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def processRequest(self):
        return Response("s")