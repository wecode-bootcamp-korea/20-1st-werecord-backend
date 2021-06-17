import json
import bcrypt
import jwt
import requests
import boto3
import time

from datetime              import datetime

from django.views          import View
from django.http           import JsonResponse

from json.decoder          import JSONDecodeError

from my_settings           import SECRET, ALGORITHM, JWT_DURATION_SEC
from werecord.settings     import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from users.models          import User, UserType, Batch

# 로그인
class GoogleLoginView(View):
    def get(self, request):
        id_token     = request.headers.get('Authorization', None)

        if not id_token:
            return JsonResponse({'message': 'ID_TOKEN_REQUIRED'}, status=401)

        if not id_token:
                return JsonResponse({'message': 'ACCESS_TOKEN_REQUIRED'}, status=401)

        user_request = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        user_info    = user_request.json()

        if not user_info:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        login_user, created = User.objects.get_or_create(
            google_login_id   = user_info['sub'],
            email             = user_info['email'],
            profile_image_url = user_info['picture'],
        )

        werecord_token = jwt.encode(
                {
                    'user_id'  : login_user.id,
                    'iat'      : int(time.time()),
                    'exp'      : int(time.time()) + JWT_DURATION_SEC
                }, SECRET['secret'],ALGORITHM
        )

        if created is False and login_user.user_type.name is '2':
            user_info = {
                'user_id'   : login_user.id,
                'user_type' : login_user.user_type.name,
                'batch'     : login_user.batch.name
            }

        elif created is False and login_user.user_type.name is '1':
            user_info = {
                'user_id'   : login_user.id,
                'user_type' : login_user.user_type.name,
                'batch'     : ''
            }

        elif created is True:
            user_info = ''

        return JsonResponse({'user_info' : user_info, 'werecord_token' : werecord_token}, status=200)