from django.urls   import path

from records.views import RecordCheckView, PutButtonView

urlpatterns = [
    path('', RecordCheckView.as_view()),
    path('/<int:type_id>', PutButtonView.as_view())
]