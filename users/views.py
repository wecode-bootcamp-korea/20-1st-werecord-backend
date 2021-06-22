import json
import jwt
import requests
import time
import datetime

from json.decoder      import JSONDecodeError
from datetime          import date

from django.views      import View
from django.http       import JsonResponse

from my_settings       import SECRET, ALGORITHM, JWT_DURATION_SEC
from users.models      import User
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
                    'iat'      : int(time.time()),
                    'exp'      : int(time.time()) + JWT_DURATION_SEC
                }, SECRET['secret'],ALGORITHM
        )

        user_info = {
            'user_type'        : login_user.user_type.name if login_user.user_type else "",
            'batch'            : login_user.batch.name if login_user.batch else "",
            "email'"           : user_info.get('email') if user_info.get('email') else "",
            "profile_image_url": user_info.get('picture') if user_info.get('picture') else "",
        }

        return JsonResponse({'user_info' : user_info, 'werecord_token' : werecord_token}, status=200)

class StudentView(View):
    @login_required
    def get(self, request):
        user = request.user

        if not user.user_type.id == 2:
            return JsonResponse({'message': 'UNAUTHORIZED_USER_ERROR'}, status = 400)

        user      = User.objects.select_related('batch').prefetch_related('record_set').get(id=user.id)
        records   = user.record_set.filter(user_id=user.id)
        now       = datetime.datetime.now()
        time_gap  = datetime.timedelta(seconds=32406)
        now_korea = now + time_gap

        start_sum   = 0
        start_count = 0
        end_sum     = 0
        end_count   = 0

        for record in records:
            standard_time     = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)

            if record.start_at:
                total         = (record.start_at-standard_time).total_seconds()
                start_sum    += total
                start_count  += 1
            if record.end_at:
                total         = (record.end_at-standard_time).total_seconds()
                end_sum      += total
                end_count    += 1

        today          = now_korea.isocalendar()
        week_start_day = date.fromisocalendar(today.year, today.week, 1)
        week_end_day   = week_start_day + datetime.timedelta(days=6)
        week_records   = records.filter(end_at__date__range=[week_start_day, week_end_day])

        weekly_records     = {f'{record.end_at.weekday()}': record.oneday_time for record in week_records}
        full_weekly_record = {week_number : weekly_records[str(week_number)] \
                                if str(week_number) in weekly_records.keys() else 0 for week_number in range(5)}
                    
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
                                'weekly_record'            : full_weekly_record,
                                'total_accumulate_records' : total_accumulate_record_result,
                                'average_start_time'       : str(datetime.timedelta(seconds=start_sum/start_count)),
                                'average_end_time'         : str(datetime.timedelta(seconds=end_sum/end_count)),
                                'wecode_d_day'             : (now_korea.date()-user.batch.start_day).days

                    }
        }

        return JsonResponse({'result': result}, status = 200)