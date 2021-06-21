from django.urls import path

from users.views import GoogleLoginView, UserInfoView, BatchInfomationView, MentorPageView, StudentPageView, BatchPageView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/info", UserInfoView.as_view()),
    path("/info/<int:user_id>", UserInfoView.as_view()),
    path("/batch-info", BatchInfomationView.as_view()),
    path("/mentor", MentorPageView.as_view()),
    path("/student", StudentPageView.as_view()),
    path("/batch/<int:batch_id>", BatchPageView.as_view()),
]