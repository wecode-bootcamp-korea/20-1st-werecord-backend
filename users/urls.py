from django.urls import path
from users.views import GoogleLoginView


urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
]