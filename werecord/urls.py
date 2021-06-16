from django.contrib import admin
from django.urls    import path, include

urlpatterns = [
    path("users", include("users.urls")),
    path("records", include("records.urls")),
]
