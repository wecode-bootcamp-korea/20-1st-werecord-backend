from django.urls import path

from users.views import GoogleLoginView, StudentView, BatchView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/student", StudentView.as_view()),
    path("/batch/<int:batch_id>", BatchView.as_view()),
]