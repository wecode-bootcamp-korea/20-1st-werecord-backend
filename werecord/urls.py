from django.urls import path, include

from ping        import PingView

urlpatterns = [
    path("users", include("users.urls")),
    path("records", include("records.urls")),
    path("ping", PingView.as_view())
]