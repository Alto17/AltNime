from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")),
    path("", include("home.urls"), name="home"),
    path("accounts/", include("accounts.urls")),
]
