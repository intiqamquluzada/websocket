from django.urls import path
from chat.views import *

urlpatterns = [
    path("selection/", index_view, name='index'),
    path("<str:room_name>/", room_view, name='room'),
    path("", login_view, name='login'),
    path("register", register_view, name='register'),
]