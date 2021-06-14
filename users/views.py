import json
import datetime

from datetime         import date
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.models     import User, Batch

class MyPageView(View):
    # @login_confirm
    def get(self, request):
        user = request.user

        if user.user_type.id == 1:
            now       = datetime.datetime.now()
            time_gap  = datetime.timedelta(seconds=32406)
            now_korea = now + time_gap

            q       = Q(start_day__lte=now_korea.date()) & Q(end_day__gte=now_korea.date())
            batches = Batch.objects.filter(q).order_by('-name')

            total_results = []

            for batch in batches:
                on_user_number   = 0
                user_total_times = []
                users            = User.objects.filter(batch_id=batch.id)

                for user in users:
                    user_total_times.append(user.total_time)
                    if not user.record_set.last():
                        on_user_number += 0
                    elif now_korea.date() == user.record_set.last().start_at.date() and not user.record_set.last().end_at:
                        on_user_number += 1
                    else:
                        on_user_number += 0

                result = [
                    {
                        'batch_id'                : batch.id,
                        'batch_name'              : batch.name,
                        'batch_start_day'         : batch.start_day,
                        'batch_end_day'           : batch.end_day,
                        'batch_total_time'        : sum(user_total_times),
                        'wecode_d_day'            : (now_korea.date()-batch.start_day).days,
                        'batch_on_user_number'    : on_user_number,
                        'batch_total_user_number' : len(User.objects.filter(batch_id=batch.id))

                    }
                ]

                total_results.append(result)
        
            return JsonResponse({'result': total_results}, status = 200)

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
            