from django.urls import path
from users.views import GoogleLoginView


from users.views import GoogleLoginView, MentorPageView, StudentPageView, BatchPageView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/mentor", MentorPageView.as_view()),
    path("/student", StudentPageView.as_view()),
    path("/batch/<int:batch_id>", BatchPageView.as_view())
]