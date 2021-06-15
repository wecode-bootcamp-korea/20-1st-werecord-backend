from django.urls import path

from users.views import MyPageView

urlpatterns = [
    path("/mypage/<int:user_type_id>", MyPageView.as_view())
]