from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("back/", include("core.urls")),
    # I route admin to the root
    # And I place it at the end otherwise it will override all other routes
    path("", admin.site.urls),
]
