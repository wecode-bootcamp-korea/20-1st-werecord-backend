from django.urls import path

from users.views import MentoPageView, StudentPageView, BatchPageView

urlpatterns = [
    path("/mento", MentoPageView.as_view()),
    path("/student", StudentPageView.as_view()),
    path("/batchpage/<int:batch_name>", BatchPageView.as_view())
]