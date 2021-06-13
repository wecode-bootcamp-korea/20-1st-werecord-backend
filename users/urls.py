from django.urls import path

from users.views import BatchPageView

urlpatterns = [
    path("/batchpage", BatchPageView.as_view())
]