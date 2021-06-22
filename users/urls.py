from django.urls import path

from users.views import MentorPageView

urlpatterns = [
    path("/mentor", MentorPageView.as_view()),
]