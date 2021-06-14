from django.urls import path

from users.views import BatchPageView

urlpatterns = [
    path("/batchpage/<int:batch_name>", BatchPageView.as_view())
]