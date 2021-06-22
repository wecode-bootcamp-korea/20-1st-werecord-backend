from django.urls import path

from users.views import GoogleLoginView, StudentView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/student", StudentView.as_view()),
]