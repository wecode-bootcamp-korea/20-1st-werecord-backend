import json
import datetime

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from records.models import Record
from utils.check_ip import check_ip

class RecordCheckView(View):
    # @login_confirm
    def get(self, request):
        # user = request.user
        user   = User.objects.get(id=1)
        record = Record.objects.filter(user_id=user.id).last()

        if record:
            now        = datetime.datetime.now()
            time_gap   = datetime.timedelta(seconds=32406)
            now_korea  = now + time_gap
            check_date = record.start_at.date()

            if not now_korea.date() == check_date and not record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR'}, status=400)
    
        return JsonResponse({'message': 'SUCCESS'}, status=200)

    @check_ip
    def post(self, request):
        try:
            # user = request.user
            user           = User.objects.get(id=1)
            data           = json.loads(request.body)
            record         = Record.objects.filter(user_id=user.id).last()
            date           = record.start_at
            record.end_at  = datetime.datetime(date.year, date.month, date.day, hour=data['hour'], minute=data['minute'])

            day_total_time = record.end_at - record.start_at
            if day_total_time.days < 0:
                return JsonResponse({'message': 'RECHECK_ENDTIME_ERROR'}, status=400)
            else:
                record.oneday_time = day_total_time.seconds
                record.save()
                user.total_time   += day_total_time.seconds
                user.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class PutButtonView(View):
    # @login_confirm
    @check_ip
    def get(self, request, type_id):     
        # user = request.user
        user      = User.objects.get(id=1)
        record    = Record.objects.filter(user_id=user.id).last()
        now       = datetime.datetime.now()
        time_gap  = datetime.timedelta(seconds=32406)
        now_korea = now + time_gap
        
        if type_id == 1:
            if record:
                if now_korea.date() == record.start_at.date():
                    return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

            Record.objects.create(user_id=user.id, start_at=now_korea)

            result = [
                {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'start_at'  : str(now_korea.time()),
                    'comment'   : '좋은 아침 입니다!' 
                }
            ]

            return JsonResponse({'result': result}, status=201)

        if type_id == 2:
            if not record:
                return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)
            if record.end_at and now_korea.date() == record.end_at.date():
                return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)
            if record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

            record.end_at = now_korea

            day_total_time = record.end_at - record.start_at
            if 0 < day_total_time.seconds <= 60:
                return JsonResponse({'message': 'CLOSE_TIME_ERROR'}, status=400)
            else:
                record.oneday_time = day_total_time.seconds
                record.save()
                user.total_time   += day_total_time.seconds
                user.save()
            
            result = [
                {
                    'user_id'          : user.id,
                    'user_name'        : user.name,
                    'user_oneday_time' : record.oneday_time,
                    'comment'          : '오늘 하루도 수고하셨습니다!' 
                }
            ]

            return JsonResponse({'result': result}, status=201)