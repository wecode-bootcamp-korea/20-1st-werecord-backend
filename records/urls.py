from django.urls   import path

from records.views import RecordCheckView, RecordStartTimeView

urlpatterns = [
    path('', RecordCheckView.as_view()),
    path('/start', RecordStartTimeView.as_view()),
]