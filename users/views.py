import json
import jwt
import requests
import datetime
import time
import boto3
import uuid

from json.decoder      import JSONDecodeError
from datetime          import date

from django.views      import View
from django.http       import JsonResponse

from my_settings       import SECRET, ALGORITHM
from werecord.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from users.models      import User, UserType, Batch, Position
from utils.decorator   import login_required 

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
                    'iat'      : datetime.datetime.now().timestamp()
                }, SECRET['secret'],ALGORITHM
        )

        user_info = {
            "user_id"          : login_user.google_login_id if created == False else "",
            'user_type'        : login_user.user_type.name if login_user.user_type else "",
            'batch'            : login_user.batch.name if login_user.batch else "",
            "email"            : user_info.get('email') if user_info.get('email') else "",
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

        user = request.user

        data  = {
                'profile_image_url': user.profile_image_url,
                'name'             : user.name,
                'user_type'        : user.user_type.name if user.user_type else "",
                'batch'            : user.batch.name if user.batch else "",
                'position'         : user.position.name if user.position else "",
                'blog'             : user.blog,
                'github'           : user.github,
                'birthday'         : user.birthday,
        }
        return JsonResponse({'data':data}, status =201)

    @login_required
    def post(self, request):
        try:
            data = json.loads(request.POST['info'])

            user = request.user 

            image = request.FILES.get('image')

            if image is None:
                image_url = data.get("profile_image_url") if data.get("profile_image_url") else user.profile_image_url

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

                s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
                s3_image = s3.Object("werecord", user.profile_image_url[49:])
                if s3_image.key:
                    s3_image.delete()

                image_url = "https://werecord.s3.ap-northeast-2.amazonaws.com/" + my_uuid
            
            user.profile_image_url = image_url

            user.name              = data.get("name")
            user.email             = data.get("email") if data.get("email") else user.email
            user.user_type         = UserType.objects.get(name = data.get('user_type'))
            user.batch             = Batch.objects.get(name = data.get("batch")) if data.get("batch") else None
            user.position          = Position.objects.get(name = data.get("position"))
            user.blog              = data.get("blog")
            user.github            = data.get("github")
            user.birthday          = data.get("birthday") if data.get("birthday") != "" else None
            user.save()

            user_info = {
                'user_type' : user.user_type.name,
                'batch'     : user.batch.name if user.batch else ''
            }

            return JsonResponse({'user_info': user_info, 'message': 'SUCCESS'}, status =201)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)     

    @login_required
    def delete(self, request):

        s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
        s3_image = s3.Object("werecord", request.user.profile_image_url[49:])
        if s3_image.key:
            s3_image.delete()

        request.user.delete()
        
        return JsonResponse({"message": "SUCCESS"}, status=204)  

class StudentView(View):
    @login_required
    def get(self, request):
        user = request.user

        if not user.user_type.id == 2:
            return JsonResponse({'message': 'UNAUTHORIZED_USER_ERROR'}, status = 400)

        user      = User.objects.select_related('batch').prefetch_related('record_set').get(id=user.id)
        records   = user.record_set.all()
        now_korea = datetime.datetime.now() + datetime.timedelta(seconds=32406)

        WEEK_DAYS = 5

        today          = now_korea.isocalendar()
        week_start_day = date.fromisocalendar(today.year, today.week, 1)
        week_end_day   = week_start_day + datetime.timedelta(days=6)
        week_records   = records.filter(end_at__date__range=[week_start_day, week_end_day])

        week_oneday_time       = {f'{record.end_at.weekday()}': record.oneday_time for record in week_records}
        total_week_oneday_time = {week_number : week_oneday_time[str(week_number)] \
                                if str(week_number) in week_oneday_time.keys() else 0 for week_number in range(WEEK_DAYS)}
                    
        total_accumulate_record_result = []
        oneday_time_sum = 0
        for record in records:
            if record.end_at:
                oneday_time_sum += record.oneday_time
                total_accumulate_record_result.append(oneday_time_sum)

        result = {
                    'user_information' : {
                                'user_id'                : user.id,
                                'user_name'              : user.name,
                                'user_profile_image_url' : user.profile_image_url,
                                'user_total_time'        : user.total_time
                    },
                    'record_information' : {
                                'weekly_record'            : total_week_oneday_time,
                                'total_accumulate_records' : total_accumulate_record_result,
                                'average_start_time'       : str(user.average_start) if user.average_start else 0,
                                'average_end_time'         : str(user.average_end) if user.average_end else 0,
                                'wecode_d_day'             : (now_korea.date() - user.batch.start_day).days

                    }
        }

        return JsonResponse({'result': result}, status = 200)

class BatchView(View):
    @login_required
    def get(self, request, batch_id):
        user = request.user

        if user.user_type_id == 2 and not user.batch.id == batch_id:
            return JsonResponse({'message': 'NOT_YOUR_BATCH_ERROR'}, status = 400)

        winner_batch    = Batch.objects.all().order_by('-total_time').first()
        my_batch        = Batch.objects.get(id=batch_id)
        my_batch_users  = User.objects.filter(batch_id=my_batch.id).order_by('name')
        my_batch_mentor = User.objects.get(name=my_batch.mentor_name, user_type_id=1) \
                            if User.objects.filter(name=my_batch.mentor_name, user_type_id=1).exists() else None
        now_korea       = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        
        GOST_RANKING = 3

        today               = now_korea.isocalendar()
        last_week_start_day = date.fromisocalendar(today.year, today.week-1, 1)
        last_week_end_day   = last_week_start_day + datetime.timedelta(days=6)

        compare_times = []
        for user in my_batch_users:
            records              = user.record_set.filter(end_at__date__range=[last_week_start_day, last_week_end_day])
            last_week_total_time = 0
            for record in records:
                last_week_total_time += record.oneday_time if record.oneday_time else 0
            compare_times.append(last_week_total_time)
        
        ranking_results = []
        if len(compare_times) < GOST_RANKING:
            ranking_times = sorted(compare_times, reverse=True)
        else:
            ranking_times = sorted(compare_times, reverse=True)[:GOST_RANKING]

        for ranking_time in ranking_times:
            if not ranking_time == 0:
                user_informaion = {}
                index_number = compare_times.index(ranking_time)
                user_informaion['user_id']                   = my_batch_users[index_number].id
                user_informaion['user_name']                 = my_batch_users[index_number].name
                user_informaion['user_last_week_total_time'] = ranking_time
                ranking_results.append(user_informaion)
        
        result = {
                    'winner_batch_information' : {
                                'winner_batch_name'       : winner_batch.name,
                                'winner_batch_total_time' : winner_batch.total_time
                    },
                    'my_batch_information' : {
                                'batch_id'         : my_batch.id,
                                'batch_name'       : my_batch.name,
                                'batch_total_time' : my_batch.total_time,
                                'ghost_ranking'    : ranking_results,
                                'peers' : [
                                        {
                                            'peer_id'                : user.id,
                                            'peer_name'              : user.name,
                                            'peer_profile_image_url' : user.profile_image_url,
                                            'peer_position'          : user.position.name,
                                            'peer_email'             : user.email,
                                            'peer_blog'              : user.blog if user.blog else None,
                                            'peer_github'            : user.github if user.github else None,
                                            'peer_birthday'          : user.birthday if user.birthday else None,
                                            'peer_status'            : False if not user.record_set.last() \
                                                                        else True if now_korea.date() == user.record_set.last().start_at.date() \
                                                                        and not user.record_set.last().end_at else False,
                                        } for user in my_batch_users
                                ],
                                'mentor' : 
                                        {
                                            'mentor_id'                : my_batch_mentor.id if my_batch_mentor else None,
                                            'mentor_name'              : my_batch_mentor.name if my_batch_mentor else my_batch.mentor_name,
                                            'mentor_profile_image_url' : my_batch_mentor.profile_image_url if my_batch_mentor else None,
                                            'mentor_position'          : my_batch_mentor.position.name if my_batch_mentor else None,
                                            'mentor_email'             : my_batch_mentor.email if my_batch_mentor else None,
                                            'mentor_blog'              : my_batch_mentor.blog if my_batch_mentor else None,
                                            'mentor_github'            : my_batch_mentor.github if my_batch_mentor else None,
                                            'mentor_birthday'          : my_batch_mentor.birthday if my_batch_mentor else None
                                        }
                    }
        }
        
        return JsonResponse({'result': result}, status = 200)

class BatchListView(View):
    @login_required
    def get(self, request):
        user    = request.user
        batches = Batch.objects.all().order_by('-id')
        
        if not user.user_type.id == 1:
            return JsonResponse({'message': 'UNAUTHORIZED_USER_ERROR'}, status = 400)

        now_korea     = datetime.datetime.now() + datetime.timedelta(seconds=32406)        
        total_results = []

        for batch in batches:
            on_user_number   = 0
            users            = User.objects.filter(batch_id=batch.id)
            batch_mentor     = User.objects.get(name=batch.mentor_name, user_type_id=1) \
                                if User.objects.filter(name=batch.mentor_name, user_type_id=1).exists() else None

            for user in users:
                if not user.record_set.last():
                    on_user_number += 0
                elif now_korea.date() == user.record_set.last().start_at.date() and not user.record_set.last().end_at:
                    on_user_number += 1
                else:
                    on_user_number += 0

            result = {
                        'batch_id'                : batch.id,
                        'batch_name'              : batch.name,
                        'mentor_id'               : batch_mentor.id if batch_mentor else None,
                        'mentor_name'             : batch_mentor.name if batch_mentor else batch.mentor_name,
                        'batch_start_day'         : batch.start_day,
                        'batch_end_day'           : batch.end_day,
                        'batch_total_time'        : batch.total_time,
                        'wecode_d_day'            : (now_korea.date() - batch.start_day).days,
                        'batch_on_user_number'    : on_user_number,
                        'batch_total_user_number' : len(users)
            }
            
            total_results.append(result)
        
        return JsonResponse({'result': total_results}, status = 200)

class CreateBatchView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            start_day = time.strptime(data['start_day'], "%Y-%m-%d")
            end_day   = time.strptime(data['end_day'], "%Y-%m-%d")

            if Batch.objects.filter(name=str(data['name'])).exists():
                return JsonResponse({'message': 'ALREADY_EXIST_ERROR'}, status=400)
            
            if not start_day < end_day:
                return JsonResponse({'message': 'RECHECK_DATE_ERROR'}, status=400)

            if not User.objects.filter(name=data['mentor_name'], user_type_id=1).exists():
                return JsonResponse({'message': 'RECHECK_MENTOR_NAME_ERROR'}, status=400)
            
            Batch.objects.create(id=int(data['name']), name=str(data['name']), 
                                start_day=data['start_day'], end_day=data['end_day'],
                                mentor_name=data['mentor_name'])

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'DATE_FORM_ERROR'}, status=400)

class ModifyBatchView(View):
    def patch(self, request, batch_id):
        try:
            data      = json.loads(request.body)
            start_day = time.strptime(data['start_day'], "%Y-%m-%d")
            end_day   = time.strptime(data['end_day'], "%Y-%m-%d")

            if not batch_id == int(data['new_batch_name']) and \
                Batch.objects.filter(name=str(data['new_batch_name'])).exists():
                return JsonResponse({'message': 'ALREADY_EXIST_ERROR'}, status=400)

            if not start_day < end_day:
                return JsonResponse({'message': 'RECHECK_DATE_ERROR'}, status=400)

            if not User.objects.filter(name=data['mentor_name'], user_type_id=1).exists():
                return JsonResponse({'message': 'RECHECK_MENTOR_NAME_ERROR'}, status=400)
            
            batch             = Batch.objects.get(id=batch_id)
            batch.id          = int(data['new_batch_name']) if data['new_batch_name'] else batch.id
            batch.name        = str(data['new_batch_name']) if data['new_batch_name'] else batch.name
            batch.start_day   = data['start_day'] if data['start_day'] else batch.start_day
            batch.end_day     = data['end_day'] if data['end_day'] else batch.end_day
            batch.mentor_name = data['mentor_name'] if data['mentor_name'] else batch.mentor_name
            batch.save()

            if data['new_batch_name'] and not batch_id == int(data['new_batch_name']):
                Batch.objects.get(id=batch_id).delete()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'DATE_FORM_ERROR'}, status=400)

    def delete(self, request, batch_id):
        if User.objects.filter(batch_id=batch_id).exists():
            return JsonResponse({'message': 'ALREADY_USED_ERROR'}, status=400)
            
        Batch.objects.get(id=batch_id).delete()

        return JsonResponse({'message': 'SUCCESS'}, status=204)