import json
import datetime

from datetime       import date
from django.http    import JsonResponse
from django.views   import View

from users.models   import User

class MyPageView(View):
    # @login_confirm
    def get(self, request):
        user = request.user

        if user.user_type.id == 1:
            return JsonResponse({'message': 'WE_NEED_MORE_TIME..!'}, status = 200)

        if user.user_type.id == 2:
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
                    
            total_accumulate_record_result = []
            oneday_time_sum = 0
            for record in records:
                if record.end_at:
                    oneday_time_sum += record.oneday_time
                    total_accumulate_record_result.append(oneday_time_sum)

            result = [
                {
                    'user_information' : {
                                'user_id'                : user.id,
                                'user_name'              : user.name,
                                'user_profile_image_url' : user.profile_image_url,
                                'user_total_time'        : user.total_time
                    },
                    'record_information' : {
                                'weekly_record'            : {f'{record.end_at.weekday()}': record.oneday_time \
                                                                for record in week_records},
                                'total_accumulate_records' : total_accumulate_record_result,
                                'average_start_time'       : str(datetime.timedelta(seconds=start_sum/start_count)),
                                'average_end_time'         : str(datetime.timedelta(seconds=end_sum/end_count)),
                                'wecode_d_day'             : (now_korea.date()-user.batch.start_day).days

                    }
                }
            ]

            return JsonResponse({'result': result}, status = 200)
            