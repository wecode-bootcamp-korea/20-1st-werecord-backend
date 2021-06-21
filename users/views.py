import json
import jwt
import requests
import boto3
import time
import uuid

from json.decoder      import JSONDecodeError
from datetime          import date

from django.views      import View
from django.http       import JsonResponse

from my_settings       import SECRET, ALGORITHM, JWT_DURATION_SEC
from werecord.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from utils.decorator   import login_required
from users.models      import User, UserType, Batch, Position

class GoogleLoginView(View):
    def get(self, request):
        id_token     = request.headers.get('Authorization', None)

        if not id_token:
            return JsonResponse({'message': 'ID_TOKEN_REQUIRED'}, status=401)

        user_request = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        user_info    = user_request.json()

        if not user_info:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        login_user, created = User.objects.get_or_create(
            google_login_id   = user_info['sub'],
        )

        werecord_token = jwt.encode(
                {
                    'user_id'  : login_user.id,
                    'iat'      : int(time.time()),
                    'exp'      : int(time.time()) + JWT_DURATION_SEC
                }, SECRET['secret'],ALGORITHM
        )

        user_info = {
            'user_id'          : login_user.id,
            'user_type'        : login_user.user_type.name if login_user.user_type else "",
            'batch'            : login_user.batch.name if login_user.batch else "",
            "email'"           : user_info.get('email') if user_info.get('email') else "",
            "profile_image_url": user_info.get('picture') if user_info.get('picture') else "",
        }

        return JsonResponse({'user_info' : user_info, 'werecord_token' : werecord_token}, status=200)

class UserInfoView(View):
    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    @login_required
    def get(self, request):

        user = User.objects.get(id = request.user)

        data  = {
                "user_id"          : user.id,
                'profile_image_url': user.profile_image_url,
                'name'             : user.name,
                'user_type'        : user.user_type.name,
                'batch'            : user.batch.name,
                'position'         : user.position.name,
                'blog'             : user.blog,
                'github'           : user.github,
                'birthday'         : user.birthday,
        }
        return JsonResponse({'data':data}, status =201)

    def post(self, request, user_id):
        try:
            data = json.loads(request.POST['info'])
            user = User.objects.get(id = user_id) 

            image = request.FILES.get('image')

            if image is None:
                image_url = user.profile_image_url

            else:
                my_uuid    = str(uuid.uuid4())

                self.s3_client.upload_fileobj(
                    image,
                    "werecord",
                    my_uuid,
                    ExtraArgs={
                        "ContentType": image.content_type
                    }
                )
        
                image_url = "https://werecord.s3.ap-northeast-2.amazonaws.com/" + my_uuid

            User.objects.filter(id = user_id).update(
                profile_image_url = image_url,
                name              = data.get('name'),
                user_type         = UserType.objects.get(name = data.get('user_type')),
                batch             = Batch.objects.get(name = data.get("batch")),
                position          = Position.objects.get(name = data.get("position")),
                blog              = data.get("blog"),
                github            = data.get("github"),
                birthday          = data.get("birthday") if data.get("birthday") is not "" else None
            )

            user      = User.objects.get(id = user_id) 
            user_info = {
                'user_id'   : user.id,
                'user_type' : user.user_type.name,
                'batch'     : user.batch.name
            }

            return JsonResponse({'user_info': user_info, 'message': 'SUCCESS'}, status =201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400) 

    @login_required
    def delete(self, request):
        
        User.objects.filter(id = request.user.id).delete()
        
        return JsonResponse({"message": "SUCCESS"}, status=204)   