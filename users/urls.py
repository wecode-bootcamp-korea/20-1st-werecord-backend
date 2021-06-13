from django.urls import path

from users.views import MyPageView

urlpatterns = [
    path("/mypage", MyPageView.as_view()),
]