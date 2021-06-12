import json
import datetime

from django.http    import JsonResponse
from django.views   import View

from users.models   import User, Batch
class BatchPageView(View):
    # @login_confirm
    def get(self, request):
        # user = request.user
        user = User.objects.get(id=1)
        # batch_id = request.GET.get('batch_id', None)
        batch_id = 1

        if user.user_type_id == 2:
            if not user.batch_id == batch_id:
                return JsonResponse({'message': 'NOT_YOUR_BATCHPAGE_ERROR'}, status = 400)

        batch    = Batch.objects.get(id=batch_id)
        users    = User.objects.filter(batch_id=batch.id)
        now      = datetime.datetime.now()
        time_gap = datetime.timedelta(seconds=32406)
        kor_time = now + time_gap

        batches           = Batch.objects.all()
        batch_total_times = []
        for batch in batches:
            users = User.objects.filter(batch_id=batch.id)
            batch_total_times.append(sum([user.total_time for user in users]))

        winner_time  = max(batch_total_times)
        for_indexing = batch_total_times.index(winner_time)
        winner_batch = batches[for_indexing]
        winner_users = User.objects.filter(batch_id=winner_batch.id)

        GOST_RANKING = 3

        if len(users) < GOST_RANKING:
            ranking_users = users.order_by('-total_time')
        else:
            ranking_users = users.order_by('-total_time')[:GOST_RANKING]
        
        result = [
            {
                'winner_batch_information' : {
                                    'winner_batch_name' : winner_batch.name,
                                    'winner_batch_total_time' : sum([user.total_time for user in winner_users])
                },
                'my_batch_information' : {
                                    'batch_id'         : batch.id,
                                    'batch_name'       : batch.name,
                                    'batch_total_time' : sum([user.total_time for user in users]),
                                    'ghosts'           : {
                                        'gold_user_id' : 
                                        'gold_user_name' : 
                                        'gold_user_total_time' : 
                                    },
                                    'peers' : [
                                        {
                                            'peer_id'                : user.id,
                                            'peer_name'              : user.name,
                                            'peer_profile_image_url' : user.profile_image_url,
                                            'peer_status'            : 'ON' if not kor_time.date() == user.record_set.last().start_at.date() and not user.record_set.last().end_at else 'OFF',
                                        } for user in users
                                    ]
                }
            }
        ]

        return JsonResponse({'result': result}, status = 200)