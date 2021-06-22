from django.urls import path

from users.views import GoogleLoginView, StudentView, BatchView, BatchListView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/student", StudentView.as_view()),
    path("/batch/<int:batch_id>", BatchView.as_view()),
    path("/batchlist", BatchListView.as_view()),
]
