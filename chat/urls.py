from django.urls import path
from chat.views import *

urlpatterns = [
    path("", index_view, name='index'),
    path("<str:room_name>/", room_view, name='room'),
]