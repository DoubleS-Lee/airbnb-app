from . import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("list", views.list_rooms),
]