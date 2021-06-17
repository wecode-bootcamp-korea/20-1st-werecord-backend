from django.urls import path

from users.views import GoogleLoginView, MentoPageView, StudentPageView, BatchPageView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/mento", MentoPageView.as_view()),
    path("/student", StudentPageView.as_view()),
    path("/batch/<int:batch_id>", BatchPageView.as_view())
]