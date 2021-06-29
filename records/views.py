import json
import datetime

from django.http     import JsonResponse
from django.views    import View

from records.models  import Record, Message
from utils.decorator import login_required
from utils.check_ip  import check_ip

class RecordCheckView(View):
    @login_required
    def get(self, request):
        user        = request.user
        now_korea   = datetime.datetime.now() + datetime.timedelta(seconds=32406)
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
        
    @login_required
    @check_ip
    def post(self, request):
        try:
            user          = request.user
            data          = json.loads(request.body)
            record        = user.record_set.last()
            standard_time = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)

            if not 0 <= data['hour'] <= 23 or not 0 <= data['minute'] <= 59:
                return JsonResponse({'message': 'TIME_FORM_ERROR'}, status=400)

            end_at = datetime.datetime(record.start_at.year, record.start_at.month, record.start_at.day, 
                                        hour=data['hour'], minute=data['minute'])

            oneday_time = end_at - record.start_at
            if oneday_time.days < 0:
                return JsonResponse({'message': 'RECHECK_ENDTIME_ERROR'}, status=400)
            
            record.end_at      = end_at
            record.oneday_time = oneday_time.seconds
            record.save()

            if not user.average_end:
                end_seconds      = (end_at-standard_time).total_seconds()
                user.average_end = str(datetime.timedelta(seconds=end_seconds))
            else:
                average_end      = end_at.replace(
                                    hour=user.average_end.hour,     minute=user.average_end.minute, 
                                    second=user.average_end.second, microsecond=user.average_end.microsecond)
                end_seconds      = ((average_end-standard_time).total_seconds() + (end_at-standard_time).total_seconds()) / 2
                user.average_end = str(datetime.timedelta(seconds=end_seconds))

            user.total_time += oneday_time.seconds
            user.save()
            user.batch.total_time += oneday_time.seconds
            user.batch.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

class RecordStartTimeView(View):
    @login_required
    @check_ip
    def post(self, request):
        user          = request.user
        record        = user.record_set.last()
        now_korea     = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        standard_time = now_korea.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if record:
            if now_korea.date() == record.start_at.date():
                return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

        Record.objects.create(user_id=user.id, start_at=now_korea)

        if not user.average_start:
            start_seconds      = (now_korea-standard_time).total_seconds()
            user.average_start = str(datetime.timedelta(seconds=start_seconds))
        else:
            average_start      = now_korea.replace(
                                    hour=user.average_start.hour,     minute=user.average_start.minute, 
                                    second=user.average_start.second, microsecond=user.average_start.microsecond)
            start_seconds      = ((average_start-standard_time).total_seconds() + (now_korea-standard_time).total_seconds()) / 2
            user.average_start = str(datetime.timedelta(seconds=start_seconds))

        user.save()

        result = {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'start_at'  : str(now_korea.time())
        }

        return JsonResponse({'result': result}, status=201)

class RecordStopTimeView(View):
    @login_required
    @check_ip
    def post(self, request):
        user          = request.user
        record        = user.record_set.last()
        now_korea     = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        standard_time = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)

        if not record:
            return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)
        if record.end_at and now_korea.date() == record.end_at.date():
            return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)
        if record.end_at:
            return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

        record.end_at = now_korea

        oneday_time = record.end_at - record.start_at
        if 0 < oneday_time.seconds <= 60:
            return JsonResponse({'message': 'CLOSE_TIME_ERROR'}, status=400)
        
        record.oneday_time = oneday_time.seconds
        record.save()

        if not user.average_end:
            end_seconds      = (now_korea-standard_time).total_seconds()
            user.average_end = str(datetime.timedelta(seconds=end_seconds))
        else:
            average_end      = now_korea.replace(
                                hour=user.average_end.hour,     minute=user.average_end.minute, 
                                second=user.average_end.second, microsecond=user.average_end.microsecond)
            end_seconds      = ((average_end-standard_time).total_seconds() + (now_korea-standard_time).total_seconds()) / 2
            user.average_end = str(datetime.timedelta(seconds=end_seconds))

        user.total_time += oneday_time.seconds
        user.save()
        user.batch.total_time += oneday_time.seconds
        user.batch.save()
            
        result = {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'comment'   : Message.objects.all().order_by('?').first().content
        }

        return JsonResponse({'result': result}, status=201)