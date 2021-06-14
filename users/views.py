import json
import datetime

from django.http    import JsonResponse
from django.views   import View
from datetime       import date

from users.models   import User, Batch

class MyPageView(View):
    # @login_confirm
    def get(self, request):
        # user = request.user
        user = User.objects.get(id=1)

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

class BatchPageView(View):
    # @login_confirm
    def get(self, request, batch_name):
        # user = request.user
        user         = User.objects.get(id=1)

        if user.user_type_id == 2:
            if not user.batch.name == batch_name:
                return JsonResponse({'message': 'NOT_YOUR_BATCHPAGE_ERROR'}, status = 400)

        my_batch       = Batch.objects.get(name=batch_name)
        my_batch_users = User.objects.filter(batch_id=my_batch.id)
        now            = datetime.datetime.now()
        time_gap       = datetime.timedelta(seconds=32406)
        now_korea      = now + time_gap

        all_batches       = Batch.objects.all()
        batch_total_times = []
        for batch in all_batches:
            batch_users = User.objects.filter(batch_id=batch.id)
            batch_total_times.append(sum([user.total_time for user in batch_users]))
        winner_total_time = max(batch_total_times)

        GOST_RANKING = 3

        today               = now_korea.isocalendar()
        last_week_start_day = date.fromisocalendar(today.year, today.week-1, 1)
        last_week_end_day   = last_week_start_day + datetime.timedelta(days=6)

        compare_times = []
        for user in my_batch_users:
            records              = user.record_set.filter(end_at__date__range=[last_week_start_day, last_week_end_day])
            last_week_total_time = 0
            for record in records:
                last_week_total_time += record.oneday_time
            compare_times.append(last_week_total_time)
        
        ranking_results = []
        if len(compare_times) < GOST_RANKING:
            ranking_times = sorted(compare_times, reverse=True)
        else:
            ranking_times = sorted(compare_times, reverse=True)[:GOST_RANKING]

        for ranking_time in ranking_times:
            user_informaion = {}
            index_number = compare_times.index(ranking_time)
            user_informaion['user_id']                   = my_batch_users[index_number].id
            user_informaion['user_name']                 = my_batch_users[index_number].name
            user_informaion['user_profile_image_url']    = my_batch_users[index_number].profile_image_url
            user_informaion['user_last_week_total_time'] = ranking_time
            ranking_results.append(user_informaion)
        
        result = [
            {
                'winner_batch_information' : {
                                'winner_batch_name'       : all_batches[batch_total_times.index(winner_total_time)].name,
                                'winner_batch_total_time' : winner_total_time
                },
                'my_batch_information' : {
                                'batch_id'         : my_batch.id,
                                'batch_name'       : my_batch.name,
                                'batch_total_time' : sum([user.total_time for user in my_batch_users]),
                                'ghost_ranking'    : ranking_results,
                                'peers' : [
                                    {
                                        'peer_id'                : user.id,
                                        'peer_name'              : user.name,
                                        'peer_profile_image_url' : user.profile_image_url,
                                        'peer_status'            : 'OFF' if not user.record_set.last() \
                                            else 'ON' if now_korea.date() == user.record_set.last().start_at.date() \
                                            and not user.record_set.last().end_at else 'OFF',
                                    } for user in my_batch_users
                                ]
                }
            }
        ]

        return JsonResponse({'result': result}, status = 200)