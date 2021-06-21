from django.urls import path

from users.views import GoogleLoginView, UserInfoView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/info", UserInfoView.as_view()),
    path("/info/<int:user_id>", UserInfoView.as_view()),
]