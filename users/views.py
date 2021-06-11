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

from users.models          import User, UserType

# 로그인
class GoogleLoginView(View):
    def post(self, request):
        try:
            access_token = request.headers.get("Authorization", None)

            # acess token이 없으면
            if not access_token:
                return JsonResponse({'message': 'ACCESS_TOKEN_REQUIRED'}, status=401)

            # 헤더로 받은 토큰을, 구글 api 주소로 header를 통해 구글에 보냄
            headers    = ({'Authorization' : f"Bearer {access_token}"})
            URL        = "https://www.googleapis.com/oauth2/v3/userinfo"
            login_data = requests.post(URL, headers=headers).json()

            # 로그인데이터가 없으면 
            if not login_data:
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

            login_user, created = User.objects.get_or_create(
                google_login_id   = login_data['sub'],
                email             = login_data['email'],
                profile_image_url = login_data['picture'],
            )
            print(created)


            # 만약 데이터가 이미 만들어진 데이터라면
            # werecord 토큰 만들기
            if created is False:
                werecord_token = jwt.encode(
                        {
                            'user_id'  : login_user.id,
                            'user_type': login_user.user_type.name,
                            'iat'      : int(time.time()),
                            'exp'      : int(time.time()) + JWT_DURATION_SEC
                        }, SECRET['secret'],ALGORITHM
                )

            # 토큰 보내기 성공
            return JsonResponse({'message' : 'SUCCESS', 'token' : werecord_token}, status=200)

        # 디코드 에러
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDecodeError"}, status=400)