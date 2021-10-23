from django.views      import View
from django.http       import JsonResponse

class PingView(View):
    def get(self, request):
        return JsonResponse({"message" : "pong"}, status=200)