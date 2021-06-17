import json
import datetime

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from records.models  import Record
from utils.decorator import login_required
from utils.check_ip  import check_ip

class RecordCheckView(View):
    @login_required
    def get(self, request):
        user        = request.user
        now         = datetime.datetime.now()
        time_gap    = datetime.timedelta(seconds=32406)
        now_korea   = now + time_gap
        record      = user.record_set.last()
        check_date  = record.start_at.date() if record else None
        user_status = False if not record \
                    else True if now_korea.date() == record.start_at.date() and not record.end_at else False

        if record and not now_korea.date() == check_date and not record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR', 'result': check_date}, status=400)
            
        result = {
                'user_id'         : user.id,
                'user_name'       : user.name,
                'user_status'     : user_status,
                'user_start_time' : record.start_at.time() if user_status else None
        }
    
        return JsonResponse({'result': result}, status=200)

    @check_ip
    def post(self, request):
        try:
            user   = request.user
            data   = json.loads(request.body)
            record = user.record_set.last()
            date   = record.start_at
            end_at = datetime.datetime(date.year, date.month, date.day, hour=data['hour'], minute=data['minute'])

            day_total_time = end_at - record.start_at
            if day_total_time.days < 0:
                return JsonResponse({'message': 'RECHECK_ENDTIME_ERROR'}, status=400)
            else:
                record.end_at      = end_at
                record.oneday_time = day_total_time.seconds
                record.save()
                user.total_time   += day_total_time.seconds
                user.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

class RecordTimeView(View):
    @login_required
    @check_ip
    def get(self, request, type_id):     
        user      = request.user
        record    = Record.objects.filter(user_id=user.id).last()
        now       = datetime.datetime.now()
        time_gap  = datetime.timedelta(seconds=32406)
        now_korea = now + time_gap
        
        if type_id == 1 and record:
            if now_korea.date() == record.start_at.date():
                return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

            Record.objects.create(user_id=user.id, start_at=now_korea)

            result = {
                        'user_id'   : user.id,
                        'user_name' : user.name,
                        'start_at'  : str(now_korea.time()),
                        'comment'   : '좋은 아침 입니다!' 
            }

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
            
            result = {
                        'user_id'          : user.id,
                        'user_name'        : user.name,
                        'user_oneday_time' : record.oneday_time,
                        'comment'          : '오늘 하루도 수고하셨습니다!' 
            }

            return JsonResponse({'result': result}, status=201)