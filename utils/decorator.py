import jwt

from django.http  import JsonResponse

from my_settings  import SECRET, ALGORITHM

from users.models import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            werecord_token = request.headers.get("Authorization", None)
            if not werecord_token:
                return JsonResponse({'message': 'LOGIN_REQUIRED'}, status=401)

            werecord_token_payload = jwt.decode(
                    werecord_token.encode('utf-8'),
                    SECRET['secret'],
                    ALGORITHM
                    )

            user = User.objects.get(id = werecord_token_payload['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        # 토큰 비정상
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_JWT'}, status=401)

        # 익명의 사용자
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
    return wrapper