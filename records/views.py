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
        user   = User.objects.get(id=2)
        record = Record.objects.filter(user_id=user.id).last()
        if record:
            now        = datetime.datetime.now()
            time_gap   = datetime.timedelta(seconds=32406)
            kor_time   = now + time_gap
            check_date = record.start_at.date()

            if not kor_time.date() == check_date and not record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR'}, status=400)
    
        return JsonResponse({'message': 'SUCCESS'}, status=200)

    # @check_ip
    def post(self, request):
        # 받아올 값 : hour(0넣으면안되고24시간으로), minute  
        # 하루 누적 시간 : 초 단위

        # user = request.user
        user          = User.objects.get(id=2)
        # data          = json.loads(request.body)
        record        = Record.objects.filter(user_id=user.id).last()

        mock = {'hour': 20, 'minute': 23}
        record.end_at = datetime.datetime(record.start_at.year, record.start_at.month, record.start_at.day, \
                                        hour=mock['hour'], minute=mock['minute'])

        day_total_time = record.end_at - record.start_at
        if day_total_time.days < 0:
            return JsonResponse({'message': 'RECHECK_ENDTIME_ERROR'}, status=400)
        else:
            record.oneday_time = day_total_time.seconds
            record.save()
            user.total_time   += day_total_time.seconds
            user.save()

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class PutButtonView(View):
    # @login_confirm
    # @check_ip
    def get(self, request, type_id):     
        # 받을값 type_id == 1 : start, type_id == 2 : end
        # 잘못 퇴근 누르는걸 막으려면 몇 초를 막아놓을까? 지금은 60초
        # 출퇴근 눌렀을 때 뜨는 메세지 포함시키기!!

        # user = request.user
        user     = User.objects.get(id=2)
        record   = Record.objects.filter(user_id=user.id).last()
        now      = datetime.datetime.now()
        time_gap = datetime.timedelta(seconds=32406)
        kor_time = now + time_gap
        
        if type_id == 1:
            if record:
                if record.start_at.date() == kor_time.date():
                    return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

            Record.objects.create(user_id=user.id, start_at=kor_time)

            result = [
                {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'start_at'  : str(kor_time.time())
                }
            ]

            comment = '좋은 아침 입니다!'

            return JsonResponse({'message': 'SUCCESS', 'result': result, 'comment': comment}, status=201)

        if type_id == 2:
            if not record:
                return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)
            if record.end_at and kor_time.date() == record.end_at.date():
                return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)
            if record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

            record.end_at = kor_time

            day_total_time = record.end_at - record.start_at
            if 0 < day_total_time.seconds <= 60:
                return JsonResponse({'message': 'CLOSE_TIME_ERROR'}, status=400)
            else:
                record.oneday_time = day_total_time.seconds
                record.save()
                user.total_time   += day_total_time.seconds
                user.save()
            
            comment = '오늘 하루도 수고하셨습니다!'

            return JsonResponse({'message': 'SUCCESS', 'comment': comment}, status=201)