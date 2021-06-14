from django.urls import path

from users.views import MyPageView, BatchPageView

urlpatterns = [
    path("/mypage", MyPageView.as_view()),
    path("/batchpage/<int:batch_name>", BatchPageView.as_view())
]