import json

from django.http import JsonResponse

def check_ip(original_function):

    def wrapper(self, request, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        
        if not user_ip == "211.106.114.186":
            return JsonResponse({'message': 'LOCATION_ERROR'}, status=400)

        return original_function(self, request, **kwargs)

    return wrapper