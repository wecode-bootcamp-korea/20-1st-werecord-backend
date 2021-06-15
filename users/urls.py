from django.urls import path

from users.views import MyPageView, BatchPageView

urlpatterns = [
    path("/mypage/<int:user_type_id>", MyPageView.as_view()),
    path("/batchpage/<int:batch_name>", BatchPageView.as_view())
]