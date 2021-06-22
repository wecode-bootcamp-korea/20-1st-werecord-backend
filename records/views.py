import json
import datetime

from django.http     import JsonResponse
from django.views    import View

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

            if not 0 <= data['hour'] <= 23 or not 0 <= data['minute'] <= 59:
                return JsonResponse({'message': 'TIME_FORM_ERROR'}, status=400)

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

class RecordStartTimeView(View):
    @login_required
    @check_ip
    def post(self, request):
        user      = request.user
        record    = user.record_set.last()
        now       = datetime.datetime.now()
        time_gap  = datetime.timedelta(seconds=32406)
        now_korea = now + time_gap
        
        if record:
            if now_korea.date() == record.start_at.date():
                return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

        Record.objects.create(user_id=user.id, start_at=now_korea)

        result = {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'start_at'  : str(now_korea.time())
        }

        return JsonResponse({'result': result}, status=201)