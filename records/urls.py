from django.urls   import path

from records.views import RecordCheckView, RecordStartTimeView, RecordStopTimeView

urlpatterns = [
    path('', RecordCheckView.as_view()),
    path('/start', RecordStartTimeView.as_view()),
    path('/stop', RecordStopTimeView.as_view()),
]