import jwt
import datetime

from django.http  import JsonResponse

from my_settings  import SECRET, ALGORITHM, ACCESS_EXPIRATION_DELTA, REFRESH_EXPIRATION_DELTA

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
            now = datetime.datetime.now().timestamp()
            if now > werecord_token_payload['iat'] + ACCESS_EXPIRATION_DELTA:
                refresh_token_payload = jwt.decode(
                        user.refresh_token,
                        SECRET['secret'],
                        ALGORITHM
                        )
        
                if now > refresh_token_payload['iat'] + REFRESH_EXPIRATION_DELTA:
                    return JsonResponse({'message': 'REFRESH_TOKEN_EXPIRED'}, status=401)

                else:
                    werecord_token = jwt.encode(
                        {
                            'user_id': user.id,
                            'iat'    : datetime.datetime.now().timestamp()
                        },
                        SECRET['secret'],
                        ALGORITHM
                        )
                    return JsonResponse({'message': 'WERECORD_TOKEN_REFRESHED', 'WERECORD_TOKEN': werecord_token}, status=401)
    
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_JWT'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
    return wrapper