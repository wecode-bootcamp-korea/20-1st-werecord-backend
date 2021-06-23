from django.urls import path

from users.views import GoogleLoginView, UserInfoView, StudentView, BatchView, BatchListView, CreateBatchView, ModifyBatchView

urlpatterns = [
    path("/login", GoogleLoginView.as_view()),
    path("/info", UserInfoView.as_view()),
    path("/student", StudentView.as_view()),
    path("/batch/<int:batch_id>", BatchView.as_view()),
    path("/batchlist", BatchListView.as_view()),
    path("/batch-manager", CreateBatchView.as_view()),
    path("/batch-manager/<int:batch_id>", ModifyBatchView.as_view()),
]