from django.urls   import path

from records.views import RecordCheckView, RecordStartView, RecordPauseView, RecordRestartView, RecordStopView

urlpatterns = [
    path('', RecordCheckView.as_view()),
    path('/start', RecordStartView.as_view()),
    path('/pause', RecordPauseView.as_view()),
    path('/restart', RecordRestartView.as_view()),
    path('/stop', RecordStopView.as_view()),
]