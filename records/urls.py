from django.urls   import path

from records.views import RecordCheckView

urlpatterns = [
    path('', RecordCheckView.as_view()),
]