from django.urls   import path

from records.views import RecordCheckView, RecordTimeView

urlpatterns = [
    path('', RecordCheckView.as_view()),
    path('/<int:type_id>', RecordTimeView.as_view())
]