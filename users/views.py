import json
import datetime

from json.decoder      import JSONDecodeError

from django.views      import View
from django.http       import JsonResponse

from utils.decorator   import login_required
from users.models      import User, Batch

class MentorPageView(View):
    @login_required
    def get(self, request):
        user    = request.user
        batches = Batch.objects.all().order_by('-name')
        
        if not user.user_type.id == 1:
            return JsonResponse({'message': 'UNAUTHORIZED_USER_ERROR'}, status = 400)

        now       = datetime.datetime.now()
        time_gap  = datetime.timedelta(seconds=32406)
        now_korea = now + time_gap
        
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

            result = {
                        'batch_id'                : batch.id,
                        'batch_name'              : batch.name,
                        'mentor_id'               : User.objects.get(name=batch.mentor_name).id,
                        'mentor_name'             : User.objects.get(name=batch.mentor_name).name,
                        'batch_start_day'         : batch.start_day,
                        'batch_end_day'           : batch.end_day,
                        'batch_total_time'        : sum(user_total_times),
                        'wecode_d_day'            : (now_korea.date()-batch.start_day).days,
                        'batch_on_user_number'    : on_user_number,
                        'batch_total_user_number' : len(User.objects.filter(batch_id=batch.id))
            }
            
            total_results.append(result)
        
        return JsonResponse({'result': total_results}, status = 200)