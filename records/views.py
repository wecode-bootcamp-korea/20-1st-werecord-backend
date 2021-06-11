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
        self.record = Record.objects.filter(user_id=user.id).last()
        if self.record:
            now        = datetime.datetime.now()
            time_gap   = datetime.timedelta(seconds=32406)
            kor_time   = now + time_gap
            today      = str(kor_time).split(' ')[0]
            self.check_date = str(self.record.start_at).split(' ')[0]

            if not today == self.check_date and not self.record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_ENDTIME_ERROR'}, status=403)
    
        return JsonResponse({'message': 'SUCCESS'}, status=200)

    @check_ip
    def post(self, request):
        # 받아올 값 : hour(0넣으면안되고24시간으로), minute  
        # 하루 누적 시간 : 초 단위

        # user = request.user
        user  = User.objects.get(id=2)
        # data  = json.loads(request.body)     

        date  = self.check_date.split('-')
        year  = int(date[0])
        month = int(date[1])
        day   = int(date[2])

        mock          = {'hour':8, 'minute':23}
        self.record.end_at = datetime.datetime(year, month, day, hour=mock['hour'], minute=mock['minute'])

        day_total_time = self.record.end_at - self.record.start_at
        if day_total_time.days < 0:
            return JsonResponse({'message': 'IMPOSSIBLE_TINE_ERROR'}, status=400)
        else:
            self.record.oneday_time = day_total_time.seconds
            self.record.save()

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class PutButtonView(View):
    # @login_confirm
    @check_ip
    def get(self, request, type_id):     
        # 받을값 type_id == 1 : start, type_id == 2 : end
        # 잘못 퇴근 누르는걸 막으려면 몇 초를 막아놓을까? 지금은 60초
        # 출퇴근 눌렀을 때 뜨는 메세지 포함시키기!!

        # user = request.user
        user   = User.objects.get(id=2)
        record = Record.objects.filter(user_id=user.id).last()

        now      = datetime.datetime.now()
        time_gap = datetime.timedelta(seconds=32406)
        kor_time = now + time_gap
        
        if type_id == 1:
            if record:
                check_date = str(record.start_at).split(' ')[0]
                today      = str(kor_time).split(' ')[0]

                if check_date == today:
                    return JsonResponse({'message': 'ALREADY_RECORD_ERROR'}, status=400)

            Record.objects.create(user_id=user.id, start_at=kor_time)
            result = [
                {
                    'user_id'   : user.id,
                    'user_name' : user.name,
                    'start_at'  : str(kor_time).split(' ')[1]
                }
            ]

            return JsonResponse({'message': 'SUCCESS', 'result': result}, status=201)

        if type_id == 2:
            if not record or record.end_at:
                return JsonResponse({'message': 'NEED_TO_RECORD_STARTTIME_ERROR'}, status=400)

            record.end_at = kor_time

            oneday_time = record.end_at - record.start_at
            if 0 < oneday_time.seconds <= 60:
                return JsonResponse({'message': 'CLOSE_TIME_ERROR'}, status=400)
            else:
                record.oneday_time = oneday_time.seconds
                record.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)