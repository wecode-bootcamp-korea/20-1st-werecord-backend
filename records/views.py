import json
import datetime

from django.http     import JsonResponse
from django.views    import View

from records.models  import DailyRecord, Record, Message
from utils.decorator import login_required
from utils.check_ip  import check_ip

class RecordCheckView(View):
    @login_required
    def get(self, request):
        user        = request.user
        now_korea    = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        record       = user.record_set.last()
        start_record = user.record_set.filter(start_at__date=now_korea.date()).first() 
        check_date   = record.start_at.date() if record else None
        check_stop   = user.dailyrecord_set.last()
        user_status  = False if not record else True if now_korea.date() == record.start_at.date() and not record.end_at else False

        if record and not now_korea.date() == check_date and not record.end_at:
            return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR', 'result': check_date}, status=400)
            
        result = {
                    'user_id'         : user.id,
                    'user_name'       : user.name,
                    'user_status'     : user_status,
                    'user_start_time' : start_record.start_at.time() if user_status else None,
                    'start_status'    : False if not record else True if now_korea.date() == check_date else False,
                    'stop_status'     : False if not check_stop else True if now_korea.date() == check_stop.date else False
        }
    
        return JsonResponse({'result': result}, status=200)
        
    @login_required
    def post(self, request):
        try:
            user          = request.user
            data          = json.loads(request.body)
            record        = user.record_set.last()
            records       = user.record_set.filter(start_at__date=record.start_at.date())
            standard_time = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)

            if not 0 <= data['hour'] <= 23 or not 0 <= data['minute'] <= 59:
                return JsonResponse({'message': 'TIME_FORM_ERROR'}, status=400)

            end_at = datetime.datetime(record.start_at.year, record.start_at.month, record.start_at.day, hour=data['hour'], minute=data['minute'])

            time_check = end_at - record.start_at
            if time_check.days < 0:
                return JsonResponse({'message': 'RECHECK_ENDTIME_ERROR'}, status=400)
            
            record.end_at         = end_at
            record.residence_time = (end_at - record.start_at).seconds
            record.save()

            if not user.average_end:
                end_seconds      = (end_at-standard_time).total_seconds()
                user.average_end = str(datetime.timedelta(seconds=end_seconds))
            else:
                average_end      = end_at.replace(
                                    hour=user.average_end.hour, minute=user.average_end.minute, 
                                    second=user.average_end.second, microsecond=user.average_end.microsecond)
                end_seconds      = ((average_end-standard_time).total_seconds() + (end_at-standard_time).total_seconds()) / 2
                user.average_end = str(datetime.timedelta(seconds=end_seconds))

            user.total_time += (end_at - record.start_at).seconds
            user.save()
            user.batch.total_time += (end_at - record.start_at).seconds
            user.batch.save()

            daily_total_time = 0
            for record in records:
                daily_total_time += (record.end_at - record.start_at).seconds
            
            DailyRecord.objects.create(user_id=user.id, date=record.start_at.date(), total_time=daily_total_time)

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)

class RecordStartView(View):
    @login_required
    @check_ip
    def post(self, request):
        user          = request.user
        now_korea     = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        standard_time = now_korea.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if user.record_set.filter(start_at__date=now_korea.date()).exists():
            return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

        Record.objects.create(user_id=user.id, start_at=now_korea)

        if not user.average_start:
            start_seconds      = (now_korea-standard_time).total_seconds()
            user.average_start = str(datetime.timedelta(seconds=start_seconds))
        else:
            average_start      = now_korea.replace(
                                    hour=user.average_start.hour, minute=user.average_start.minute, 
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

class RecordPauseView(View):
    @login_required
    def post(self, request):
        user      = request.user
        record    = user.record_set.last()
        now_korea = datetime.datetime.now() + datetime.timedelta(seconds=32406)

        if not record or (not now_korea.date() == record.start_at and record.end_at):
            return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

        if now_korea.date() == record.start_at and record.end_at:
            return JsonResponse({'message': 'NEED_TO_RECORD_RESTARTTIME_ERROR'}, status=400)

        record.end_at = now_korea

        record.residence_time = (now_korea - record.start_at).seconds
        record.save()

        user.total_time += (now_korea - record.start_at).seconds
        user.save()
        user.batch.total_time += (now_korea - record.start_at).seconds
        user.batch.save()

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class RecordRestartView(View):
    @login_required
    @check_ip
    def post(self, request):
        user      = request.user
        record    = user.record_set.last()
        now_korea = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        
        if not record or not now_korea.date() == record.start_at.date():
            return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

        if not record.end_at:
            return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR'}, status=400)

        Record.objects.create(user_id=user.id, start_at=now_korea)

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class RecordStopView(View):
    @login_required
    @check_ip
    def post(self, request):
        user          = request.user
        now_korea     = datetime.datetime.now() + datetime.timedelta(seconds=32406)
        record        = user.record_set.last()
        records       = user.record_set.filter(start_at__date=now_korea.date())
        standard_time = record.start_at.replace(hour=0, minute=0, second=0, microsecond=0)

        if not record or not records.exists():
            return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)
            
        if records.exists() and record.end_at:
            end_at = record.end_at
        else:
            end_at                = now_korea
            record.end_at         = end_at
            record.residence_time = (end_at - record.start_at).seconds
            record.save()

            user.total_time += (end_at - record.start_at).seconds
            user.save()
            user.batch.total_time += (end_at - record.start_at).seconds
            user.batch.save()

        if not user.average_end:
            end_seconds      = (end_at-standard_time).total_seconds()
            user.average_end = str(datetime.timedelta(seconds=end_seconds))
            user.save()
        else:
            average_end      = end_at.replace(
                                hour=user.average_end.hour, minute=user.average_end.minute, 
                                second=user.average_end.second, microsecond=user.average_end.microsecond)
            end_seconds      = ((average_end-standard_time).total_seconds() + (end_at-standard_time).total_seconds()) / 2
            user.average_end = str(datetime.timedelta(seconds=end_seconds))
            user.save()

        daily_total_time = 0
        for record in records:
            daily_total_time += (record.end_at - record.start_at).seconds
            
        DailyRecord.objects.create(user_id=user.id, date=end_at.date(), total_time=daily_total_time)

        result = {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'comment'   : Message.objects.all().order_by('?').first().content
        }

        return JsonResponse({'result': result}, status=201)